import re
from typing import List, Tuple

from flake8.checker import Manager, FileChecker
from flake8.utils import fnmatch, filenames_from

from .._logic import get_plugin_name, get_plugin_rules, check_include, make_baseline


REX_NAME = re.compile(r"[-_.]+")


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
        for check_type, checks in self.checks.to_dictionary().items():
            for check in checks:
                for argument in paths:
                    for filename in filenames_from(argument, self.is_path_excluded):
                        checker = FlakeHellFileChecker(
                            filename=filename,
                            check_type=check_type,
                            check=check,
                            options=self.options,
                        )
                        # if checker.should_process:
                        #     continue
                        if not self._should_create_file_checker(filename=filename, argument=argument):
                            continue
                        self.checkers.append(checker)

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

        + Run everything only serial. IDK why, but it doesn't work with parallel run
        + pass checker into `_handle_results` to get plugin name.
        """
        self.run_serial()

        results_reported = results_found = 0
        for checker in self.checkers:
            results = sorted(checker.results, key=lambda tup: (tup[1], tup[2]))
            filename = checker.display_name
            with self.style_guide.processing_file(filename):
                results_reported += self._handle_results(
                    filename=filename,
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
