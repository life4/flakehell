# built-in
from collections import defaultdict
from typing import Any, Dict, List, NamedTuple, Tuple, Optional

# external
from flake8.checker import FileChecker, Manager
from flake8.utils import filenames_from, fnmatch

# app
from ._processor import FlakeHellProcessor
from .._logic import (
    Snapshot, check_include, get_exceptions, get_plugin_name, get_plugin_rules, make_baseline, prepare_cache,
)


DEFAULT_PLUGIN = 'pycodestyle'


class Result(NamedTuple):
    plugin_name: str
    error_code: str
    line_number: int
    column: int
    text: str
    line: str


class FlakeHellCheckersManager(Manager):
    """
    Patched flake8.checker.Manager to provide `plugins` support
    """
    def __init__(self, baseline: Optional[str], **kwargs):
        self.baseline = set()
        if baseline:
            with open(baseline) as stream:
                self.baseline = {line.strip() for line in stream}
        super().__init__(**kwargs)

    def make_checkers(self, paths: List[str] = None) -> None:
        """
        Reloaded checkers generator to provide one checker per file per rule.
        Original `make_checkers` provides checker per file with all rules mixed.
        It makes difficult to filter checks by codes after all.
        """
        if paths is None:
            paths = self.arguments
        if not paths:
            paths = ['.']
        prepare_cache()

        # `checkers` is list of checks to run (and then cache)
        # check is a combination of plugin and file.
        self.checkers = []
        # `snapshots` is the list of checks that have cache and should not be run
        self.snapshots = []
        for argument in paths:
            for filename in filenames_from(argument, self.is_path_excluded):
                # get checks list
                selected_checks: Dict[str, List[Dict[str, Any]]]
                selected_checks = dict(
                    ast_plugins=[],
                    logical_line_plugins=[],
                    physical_line_plugins=[],
                )
                has_checks = False
                for check_type, checks in self.checks.to_dictionary().items():
                    for check in checks:
                        should_process = self._should_process(
                            argument=argument,
                            filename=filename,
                            check_type=check_type,
                            check=check,
                        )
                        if not should_process:
                            continue
                        selected_checks[check_type].append(check)
                        has_checks = True

                # Create checker with selected checks
                if not has_checks:
                    continue
                checker = FlakeHellFileChecker(
                    filename=filename,
                    checks=selected_checks,
                    options=self.options,
                )
                # ignore files with top-level `# flake8: noqa`
                if not checker.should_process:
                    continue
                checker.snapshot = Snapshot.create(
                    checker=checker,
                    options=self.options,
                )
                if checker.snapshot.exists():
                    self.snapshots.append(checker)
                    continue
                self.checkers.append(checker)

    def _should_process(
        self, argument: str, filename: str, check_type: str, check: Dict[str, Any],
    ) -> bool:
        # do not run plugins without rules specified
        plugin_name = get_plugin_name(check)
        rules = self._get_rules(plugin_name=plugin_name, filename=filename)
        if not rules or set(rules) == {'-*'}:
            return False

        if filename == '-':
            return True
        if fnmatch(filename=filename, patterns=self.options.filename):
            return True

        if self.options._running_from_vcs:
            return False
        if self.options.diff:
            return False
        return argument == filename

    def _get_rules(self, plugin_name: str, filename: str) -> List[str]:
        rules = get_plugin_rules(
            plugin_name=plugin_name,
            plugins=self.options.plugins,
        )
        exceptions = get_exceptions(
            path=filename,
            exceptions=self.options.exceptions,
        )
        if exceptions:
            rules = rules.copy()
            rules += get_plugin_rules(
                plugin_name=plugin_name,
                plugins=exceptions,
            )
        return rules

    def report(self) -> Tuple[int, int]:
        """Reloaded report generation to filter out excluded error codes.

        + use checker.filename as path instead of checker.display_name
        + pass checker into `_handle_results` to get plugin name.
        """
        # self.run_serial()
        results_reported = results_found = 0
        for checker in self.checkers + self.snapshots:
            if not checker.results and not checker.snapshot.exists():
                continue

            # get results either from cache or actual run
            if checker.snapshot.exists():
                all_results = checker.snapshot.results
            else:
                all_results = sorted(checker.results, key=lambda tup: (tup[1], tup[2]))
                checker.snapshot.dump(all_results)

            # group results by plugin name
            grouped_results = defaultdict(list)
            for result in all_results:
                if type(result) is not Result:
                    if len(result) == 6:
                        # cache entry is deserialized into list
                        result = Result(*result)
                    else:
                        # flake8 sets custom error codes in a few places
                        # where we didn't set `_processed_plugin`
                        result = Result(DEFAULT_PLUGIN, *result)
                grouped_results[result.plugin_name].append(result)

            # get filename
            filename = checker.filename
            if filename is None or filename == '-':
                filename = self.options.stdin_display_name or 'stdin'

            with self.style_guide.processing_file(filename):
                ignored = checker.processor.parser.ignore
                for plugin_name, results in sorted(grouped_results.items()):
                    results_reported += self._handle_results(
                        filename=filename,
                        results=results,
                        plugin_name=plugin_name,
                        ignored_codes=ignored.get(plugin_name, ()),
                    )
            results_found += len(all_results)
        return (results_found, results_reported)

    def _handle_results(
        self, filename: str, results: list, plugin_name: str, ignored_codes: Tuple[str, ...],
    ) -> int:
        rules = self._get_rules(plugin_name=plugin_name, filename=filename)
        reported_results_count = 0
        for result in results:
            # Some codes are ignored for a specific parser.
            # For example, lack of blank lines for YAML parser.
            if result.error_code in ignored_codes:
                continue

            # skip baselined errors
            if self.baseline:
                digest = make_baseline(
                    path=filename,
                    context=result.line,
                    code=result.error_code,
                    line=result.line_number,
                )
                if digest in self.baseline:
                    continue

            # skip explicitly excluded codes
            if not check_include(code=result.error_code, rules=rules):
                continue

            # report
            reported_results_count += self.style_guide.handle_error(
                code=result.error_code,
                filename=filename,
                line_number=result.line_number,
                column_number=result.column,
                text=result.text,
                physical_line=result.line,
                plugin=plugin_name,
            )
        return reported_results_count


class FlakeHellFileChecker(FileChecker):
    """
    A little bit patched FileChecker to support `--safe`
    """
    snapshot: Snapshot
    _processed_plugin: str = DEFAULT_PLUGIN

    def _make_processor(self) -> Optional[FlakeHellProcessor]:
        try:
            return FlakeHellProcessor(self.filename, self.options)
        except IOError as e:
            message = '{0}: {1}'.format(type(e).__name__, e)
            self.report('E902', 0, 0, message)
            return None

    def run_checks(self) -> Tuple[str, List[Result], Dict[str, Any]]:
        if not self.processor:
            return self.filename, self.results, self.statistics
        if not self.processor.lines:
            return self.filename, self.results, self.statistics
        try:
            return super().run_checks()
        except Exception as exc:
            if self.options.safe:
                message = '{0}: {1}'.format(type(exc).__name__, exc)
                self.report('E902', 0, 0, message)
            else:
                raise
        return self.filename, self.results, self.statistics

    def run_check(self, plugin: Dict[str, Any], **arguments):
        self._processed_plugin = get_plugin_name(plugin)
        return super().run_check(plugin=plugin, **arguments)

    def report(self, error_code: Optional[str], line_number: int, column: int, text: str) -> str:
        """
        Copy-pasted `report` method to store `Result` in `self.results` instead of tuple
        and provide `plugin_name`.
        """
        if error_code is None:
            error_code, text = text.split(' ', 1)

        # If we're recovering from a problem in _make_processor, we will not
        # have this attribute.
        if hasattr(self, 'processor'):
            line = self.processor.noqa_line_for(line_number)
        else:
            line = None

        self.results.append(Result(
            plugin_name=self._processed_plugin,
            error_code=error_code,
            line_number=line_number,
            column=column,
            text=text,
            line=line,
        ))
        return error_code
