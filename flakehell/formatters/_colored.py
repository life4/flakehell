import re

from colorama import Style, Fore
from flake8.formatting.default import Default

from .._constants import COLORS

REX_TEXT = re.compile('[A-Z]+')


class ColoredFormatter(Default):
    error_format = "{path}:{row}:{col}: {code} {text}"

    def after_init(self):
        if self.options.format.lower() not in ('default', 'colored'):
            self.error_format = self.options.format

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
