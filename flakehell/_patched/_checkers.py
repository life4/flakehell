from typing import Any, Dict, List, Tuple, Optional

from flake8.checker import Manager, FileChecker
from flake8.utils import fnmatch, filenames_from

from .._logic import (
    get_plugin_name, get_plugin_rules, check_include, make_baseline,
    Snapshot, prepare_cache, get_exceptions,
)


class FlakeHellCheckersManager(Manager):
    """
    Patched flake8.checker.Manager to provide `plugins` support
    """
    def __init__(self, baseline, **kwargs):
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
                for check_type, checks in self.checks.to_dictionary().items():
                    for check in checks:
                        checker = self._make_checker(
                            argument=argument,
                            filename=filename,
                            check_type=check_type,
                            check=check,
                        )
                        if checker is None:
                            continue

                        checker.snapshot = Snapshot.create(
                            checker=checker,
                            options=self.options,
                        )
                        if checker.snapshot.exists():
                            self.snapshots.append(checker)
                            continue

                        self.checkers.append(checker)

    def _make_checker(self, argument, filename, check_type,
                      check) -> Optional['FlakeHellFileChecker']:
        # do not run plugins without rules specified
        rules = self._get_rules(check=check, filename=filename)
        if not rules or set(rules) == {'-*'}:
            return None

        if not self._should_create_file_checker(filename=filename, argument=argument):
            return None

        checker = FlakeHellFileChecker(
            filename=filename,
            check_type=check_type,
            check=check,
            options=self.options,
        )
        # check top-level `flake8: noqa`
        if not checker.should_process:
            return None
        return checker

    def _get_rules(self, check: Dict[str, Any], filename: str):
        plugin_name = get_plugin_name(check)
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

    def _should_create_file_checker(self, filename: str, argument) -> bool:
        """Filter out excluded files
        """
        if filename == '-':
            return True
        if fnmatch(filename=filename, patterns=self.options.filename):
            return True

        if self.options._running_from_vcs:
            return False
        if self.options.diff:
            return False
        return argument == filename

    def report(self) -> Tuple[int, int]:
        """Reloaded report generation to filter out excluded error codes.

        + use checker.filename as path instead of checker.display_name
        + pass checker into `_handle_results` to get plugin name.
        """
        # self.run_serial()
        results_reported = results_found = 0
        showed = set()
        for checker in self.checkers + self.snapshots:
            if not checker.results and not checker.snapshot.exists():
                continue

            # IDK why we have duplicates but let's fight it
            if checker.display_name in showed:
                continue
            showed.add(checker.display_name)

            if checker.snapshot.exists():
                results = checker.snapshot.results
            else:
                results = sorted(checker.results, key=lambda tup: (tup[1], tup[2]))
                checker.snapshot.dump(results)

            with self.style_guide.processing_file(checker.filename):
                results_reported += self._handle_results(
                    filename=checker.filename,
                    results=results,
                    check=checker.check,
                )
            results_found += len(results)
        return (results_found, results_reported)

    def _handle_results(self, filename: str, results: list, check: dict) -> int:
        plugin_name = get_plugin_name(check)
        rules = self._get_rules(check=check, filename=filename)
        reported_results_count = 0
        for (error_code, line_number, column, text, physical_line) in results:
            if self.baseline:
                digest = make_baseline(
                    path=filename,
                    context=physical_line,
                    code=error_code,
                    line=line_number,
                )
                if digest in self.baseline:
                    continue

            if not check_include(code=error_code, rules=rules):
                continue

            reported_results_count += self.style_guide.handle_error(
                code=error_code,
                filename=filename,
                line_number=line_number,
                column_number=column,
                text=text,
                physical_line=physical_line,
                plugin=plugin_name,
            )
        return reported_results_count


class FlakeHellFileChecker(FileChecker):
    """
    A little bit patched FileChecker to handle ane check per checker
    """
    snapshot = None

    def __init__(self, filename: str, check_type: str, check, options):
        self.check_type = check_type
        self.check = check
        checks = dict(ast_plugins=[], logical_line_plugins=[], physical_line_plugins=[])
        checks[check_type] = [check]
        super().__init__(filename=filename, checks=checks, options=options)

        # display_name used in run_parallel for grouping results.
        # Flake8 groups by filename, we need to group also by the check
        self.display_name = (get_plugin_name(check), check['name'], filename)

    def __repr__(self):
        return '{name}({plugin}, {filename})'.format(
            name=type(self).__name__,
            plugin=self.check['plugin_name'],
            filename=self.filename,
        )

    def run_checks(self):
        if self.processor:
            super().run_checks()
        return self.display_name, self.results, self.statistics
