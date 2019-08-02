import re

from termcolor import colored

from .._constants import ExitCodes
from .._types import CommandResult
from .._extractors import extract


REX_CODE = re.compile(r'([A-Z]+)([0-9]+)')
REX_PLACEHOLDER = re.compile(r'(\{[a-z0-9]+\}|\%[a-z])')
REX_QUOTES = re.compile(r'([\"\'\`][\w\s\:\_\-\.]+[\"\'\`])')


def show_command(argv) -> CommandResult:
    if not argv:
        return ExitCodes.NO_PLUGIN_NAME, 'no plugin name provided'
    try:
        codes = extract(argv[0])
    except ImportError as e:
        return ExitCodes.IMPORT_ERROR, 'cannot import module: {}'.format(e.args[0])
    if not codes:
        return ExitCodes.NO_CODES, 'no codes found'
    width = max(len(code) for code in codes)
    for code, info in sorted(codes.items()):
        code = REX_CODE.sub(colored(r'\1', 'blue') + colored(r'\2', 'cyan'), code)
        info = REX_QUOTES.sub(colored(r'\1', 'yellow'), info)
        info = REX_PLACEHOLDER.sub(colored(r'\1', 'green'), info)
        print('{} | {}'.format(code.ljust(width), info))
    return 0, ''
