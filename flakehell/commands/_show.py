from .._constants import ExitCodes
from .._types import CommandResult
from .._extractors import extract


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
        print('{} | {}'.format(code.ljust(width), info))
    return 0, ''
