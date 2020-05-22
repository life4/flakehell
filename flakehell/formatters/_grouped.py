# built-in
from collections import defaultdict
from typing import DefaultDict, List

# external
from flake8.statistics import Statistics
from flake8.style_guide import Violation
from termcolor import colored

# app
from .._logic import color_code, color_description
from ._colored import ColoredFormatter


class GroupedFormatter(ColoredFormatter):
    """
    Copied and modified formatter from wemake-python-styleguide.
    It's named not `wemake` to avoid conflicts with original formatter.
    """

    def after_init(self):
        super().after_init()
        self._proccessed_filenames: List[str] = []
        self._error_count = 0

    def handle(self, error: Violation) -> None:
        """Processes each :term:`violation` to print it and all related."""
        if error.filename not in self._proccessed_filenames:
            self._print_header(error.filename)
            self._proccessed_filenames.append(error.filename)

        super().handle(error)
        self._error_count += 1

    def format(self, error: Violation) -> str:
        """Called to format each individual :term:`violation`."""
        line = '  {row_col:<8} {code} {text}'.format(
            code=color_code(error.code),
            text=color_description(error.text),
            row_col='{row}:{col}'.format(
                row=colored(str(error.line_number).rjust(4), 'green'),
                col=colored(str(error.column_number).rjust(4), 'green'),
            ),
        )
        plugin = getattr(error, 'plugin', None)
        if plugin:
            line += colored(' [{}]'.format(plugin), 'grey')
        return line

    def show_statistics(self, statistics: Statistics) -> None:
        """Called when ``--statistic`` option is passed."""
        all_errors = 0
        for error_code in statistics.error_codes():
            stats_for_error_code = statistics.statistics_for(error_code)
            statistic = next(stats_for_error_code)

            count = statistic.count
            count += sum(stat.count for stat in stats_for_error_code)
            all_errors += count
            error_by_file = _count_per_filename(statistics, error_code)

            self._write(
                '{newline}{error_code}: {message}'.format(
                    newline=self.newline,
                    error_code=colored(error_code, 'white', attrs=['bold']),
                    message=statistic.message,
                ),
            )
            for filename in error_by_file:
                self._write(
                    '  {error_count:<5} {filename}'.format(
                        error_count=error_by_file[filename],
                        filename=filename,
                    ),
                )
            self._write(colored('Total: {0}'.format(count), 'white', attrs=['underline']))

        self._write(self.newline)
        self._write(colored(
            'All errors: {0}'.format(all_errors),
            'white',
            attrs=['bold', 'underline'],
        ))

    # Our own methods:

    def _print_header(self, filename: str) -> None:
        if filename.startswith('./'):
            filename = filename[2:]
        self._write(
            '{newline}{filename}'.format(
                filename=colored(filename, 'white', attrs=['bold', 'underline']),
                newline=self.newline,
            ),
        )


# Helpers:

def _count_per_filename(
    statistics: Statistics,
    error_code: str,
) -> DefaultDict[str, int]:
    filenames: DefaultDict[str, int] = defaultdict(int)
    stats_for_error_code = statistics.statistics_for(error_code)

    for stat in stats_for_error_code:
        filenames[stat.filename] += stat.count

    return filenames
