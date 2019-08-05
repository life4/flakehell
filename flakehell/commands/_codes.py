import re

from .._constants import ExitCodes
from .._logic import color_code, color_description, extract
from .._types import CommandResult


REX_CODE = re.compile(r'([A-Z]+)([0-9]+)')
REX_PLACEHOLDER = re.compile(r'(\{[a-z0-9]+\}|\%[a-z])')
REX_QUOTES = re.compile(r'([\"\'\`][\w\s\:\_\-\.]+[\"\'\`])')


def codes_command(argv) -> CommandResult:
    """Show available codes and messages for given plugin.
    """
    if not argv:
        return ExitCodes.NO_PLUGIN_NAME, 'no plugin name provided'
    if argv[0] == '--help':
        print(codes_command.__doc__)
        return 0, ''
    if len(argv) > 1:
        return ExitCodes.TOO_MANY_ARGS, 'the command accept only one argument'

    try:
        codes = extract(argv[0])
    except ImportError as e:
        return ExitCodes.IMPORT_ERROR, 'cannot import module: {}'.format(e.args[0])
    if not codes:
        return ExitCodes.NO_CODES, 'no codes found'

    width = max(len(code) for code in codes)
    for code, info in sorted(codes.items()):
        print('{code} | {info}'.format(
            code=color_code(code.ljust(width)),
            info=color_description(info),
        ))
    return 0, ''
