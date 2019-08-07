from typing import List, Tuple

from flake8.checker import Manager, FileChecker
from flake8.utils import fnmatch, filenames_from

from .._logic import get_plugin_name, get_plugin_rules, check_include, make_baseline


class FlakeHellCheckersManager(Manager):
    """
    Patched flake8.checker.Manager to provide `plugins` support
    """
    def __init__(self, baseline, **kwargs):
        self.baseline = set()
        if baseline:
            self.baseline = {line.strip() for line in open(baseline)}
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

        self.checkers = []
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
                        if checker is not None:
                            self.checkers.append(checker)

    def _make_checker(self, argument, filename, check_type, check):
        # do not run plugins without rules specified
        plugin_name = get_plugin_name(check)
        rules = get_plugin_rules(
            plugin_name=plugin_name,
            plugins=self.options.plugins,
        )
        if not rules:
            return None

        if not self._should_create_file_checker(filename=filename, argument=argument):
            return None

        checker = FlakeHellFileChecker(
            filename=filename,
            check_type=check_type,
            check=check,
            options=self.options,
        )
        # TODO: IDK why it doesn't work, sorry
        # if checker.should_process:
        #     return None
        return checker

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
        results_reported = results_found = 0
        for checker in self.checkers:
            results = sorted(checker.results, key=lambda tup: (tup[1], tup[2]))
            with self.style_guide.processing_file(checker.filename):
                results_reported += self._handle_results(
                    filename=checker.filename,
                    results=results,
                    check=checker.check,
                )
            results_found += len(results)
        return (results_found, results_reported)

    def _handle_results(self, filename: str, results: list, check: dict) -> int:
        if not results:
            return 0
        plugin_name = get_plugin_name(check)
        rules = get_plugin_rules(
            plugin_name=plugin_name,
            plugins=self.options.plugins,
        )
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
    def __init__(self, filename: str, check_type: str, check, options):
        self.check_type = check_type
        self.check = check
        checks = dict(ast_plugins=[], logical_line_plugins=[], physical_line_plugins=[])
        checks[check_type] = [check]
        super().__init__(filename=filename, checks=checks, options=options)

        # display_name used in run_parallel for grouping results.
        # Flake8 groups by filename, we need to group also by plugin name
        self.display_name = (get_plugin_name(check), filename)

    def __repr__(self):
        return '{name}({plugin}, {filename})'.format(
            name=type(self).__name__,
            plugin=self.check['plugin_name'],
            filename=self.filename,
        )

    def run_checks(self):
        super().run_checks()
        return self.display_name, self.results, self.statistics
