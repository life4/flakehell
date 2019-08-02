import re

from colorama import Style, Fore
from flake8.formatting.default import Default
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import PythonLexer

from .._constants import COLORS

REX_TEXT = re.compile('[A-Z]+')


class ColoredFormatter(Default):
    error_format = "{path}:{row}:{col}: {code} {text}"

    def after_init(self):
        if self.options.format.lower() not in ('default', 'colored'):
            self.error_format = self.options.format
        self._lexer = PythonLexer()
        self._formatter = TerminalFormatter()

    def format(self, error):
        code = error.code
        match = REX_TEXT.match(code)
        if match:
            color = COLORS.get(match.group(), COLORS['default'])
            code = color + code + Style.RESET_ALL

        filename = error.filename
        if filename.startswith('./'):
            filename = filename[2:]

        return self.error_format.format(
            code=code,
            text=error.text,
            path=filename,
            row=Fore.CYAN + str(error.line_number) + Style.RESET_ALL,
            col=Fore.CYAN + str(error.column_number) + Style.RESET_ALL,
        )

    def show_source(self, error) -> str:
        """Called when ``--show-source`` option is provided."""
        if not self._should_show_source(error):
            return ''

        formated_line = error.physical_line.lstrip()
        adjust = len(error.physical_line) - len(formated_line)

        code = highlight(
            formated_line,
            self._lexer,
            self._formatter,
        )

        return '  {code}  {pointer}^'.format(
            code=code,
            pointer=' ' * (error.column_number - 1 - adjust),
        )

    def _should_show_source(self, error) -> bool:
        return self.options.show_source and error.physical_line is not None
