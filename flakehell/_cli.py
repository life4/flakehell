import sys
from logging import getLogger
from typing import List, NoReturn

from ._constants import NAME, ExitCodes
from .commands import COMMANDS
from ._types import CommandResult


logger = getLogger(NAME)


def main(argv: List[str] = None) -> CommandResult:
    if not argv:
        return ExitCodes.NO_COMMAND, 'No command provided. Available: {}.'.format(
            ', '.join(sorted(COMMANDS)),
        )
    command_name = argv[0]
    if command_name not in COMMANDS:
        return ExitCodes.INVALID_COMMAND, 'Invalid command: {}. Available: {}.'.format(
            command_name,
            ', '.join(sorted(COMMANDS)),
        )
    return COMMANDS[command_name](argv=argv[1:])


def entrypoint(argv: List[str] = None) -> NoReturn:
    if argv is None:
        argv = sys.argv[1:]
    exit_code, msg = main(argv)
    if msg:
        logger.error(msg)
    sys.exit(exit_code)
