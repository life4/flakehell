import sys
from logging import getLogger
from typing import List, NoReturn

from ._constants import NAME, ExitCodes
from .commands import COMMANDS


logger = getLogger(NAME)


def main(argv: List[str] = None) -> NoReturn:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        logger.error('No command provided. Available: {}.'.format(', '.join(sorted(COMMANDS))))
        sys.exit(ExitCodes.NO_COMMAND)
    command_name = argv[0]
    if command_name not in COMMANDS:
        logger.error('Invalid command: {}. Available: {}.'.format(
            command_name,
            ', '.join(sorted(COMMANDS)),
        ))
        sys.exit(ExitCodes.INVALID_COMMAND)
    exit_code, msg = COMMANDS[command_name](argv=argv[1:])
    logger.error(msg)
    sys.exit(exit_code)
