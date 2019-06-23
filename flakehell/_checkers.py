import re
from typing import List, Dict

from flake8.checker import Manager, FileChecker
from flake8.utils import fnmatch, filenames_from


REX_NAME = re.compile(r"[-_.]+")


class FlakeHellCheckersManager(Manager):
    def make_checkers(self, paths=None):
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

    def _should_create_file_checker(self, filename, argument) -> bool:
        if filename == '-':
            return True
        if fnmatch(filename=filename, patterns=self.options.filename):
            return True

        if self.options._running_from_vcs:
            return False
        if self.options.diff:
            return False
        return argument == filename

    def report(self):
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

    def _handle_results(self, filename, results, check):
        if not results:
            return 0
        rules = self._get_plugin_rules(
            plugin_name=check['plugin_name'],
            plugins=self.options.plugins,
        )
        reported_results_count = 0
        for (error_code, line_number, column, text, physical_line) in results:
            if not self._check_include(code=error_code, rules=rules):
                continue
            reported_results_count += self.style_guide.handle_error(
                code=error_code,
                filename=filename,
                line_number=line_number,
                column_number=column,
                text=text,
                physical_line=physical_line,
            )
        return reported_results_count

    @staticmethod
    def _get_plugin_rules(plugin_name: str, plugins: Dict[str, List[str]]) -> List[str]:
        plugin_name = REX_NAME.sub('-', plugin_name).lower()
        # try to find exact match
        for pattern, rules in plugins.items():
            if '*' not in pattern and REX_NAME.sub('-', pattern).lower() == plugin_name:
                return rules

        # try to find match by pattern and select the longest
        best_match = (0, [])
        for pattern, rules in plugins.items():
            if not fnmatch(filename=plugin_name, patterns=[pattern]):
                continue
            match = len(pattern)
            if match > best_match[0]:
                best_match = match, rules
        if best_match[0]:
            return best_match[1]

        return []

    @staticmethod
    def _check_include(code: str, rules: List[str]) -> bool:
        include = False
        for rule in rules:
            if len(rule) < 2 or rule[0] not in {'-', '+'}:
                raise ValueError('invalid rule: `{}`'.format(rule))
        for rule in rules:
            if fnmatch(code, patterns=[rule[1:]]):
                include = rule[0] == '+'
        return include


class FlakeHellFileChecker(FileChecker):
    def __init__(self, filename, check_type, check, options):
        self.check_type = check_type
        self.check = check
        checks = dict(ast_plugins=[], logical_line_plugins=[], physical_line_plugins=[])
        checks[check_type] = [check]
        super().__init__(filename=filename, checks=checks, options=options)
