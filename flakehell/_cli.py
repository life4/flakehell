import sys
from typing import List, NoReturn

from termcolor import colored

from ._constants import ExitCodes
from .commands import COMMANDS
from ._types import CommandResult


def show_commands():
    for name, function in sorted(COMMANDS.items()):
        desc = function.__doc__.split('\n', maxsplit=1)[0]
        print('{name} | {desc}'.format(
            name=colored(name.ljust(9), 'green'),
            desc=desc,
        ))


def main(argv: List[str] = None) -> CommandResult:
    if not argv:
        show_commands()
        return ExitCodes.NO_COMMAND, 'No command provided'
    command_name = argv[0]
    if command_name in ('help', '--help', 'commands'):
        show_commands()
        return 0, ''
    if command_name not in COMMANDS:
        show_commands()
        return ExitCodes.INVALID_COMMAND, 'Invalid command: {}'.format(command_name)
    return COMMANDS[command_name](argv=argv[1:])


def entrypoint(argv: List[str] = None) -> NoReturn:
    """Default entrypoint for CLI (flakehell).
    """
    if argv is None:
        argv = sys.argv[1:]
    exit_code, msg = main(argv)
    if msg:
        print(colored(msg, 'red'))
    sys.exit(exit_code)


def flake8_entrypoint(argv: List[str] = None) -> NoReturn:
    """Entrypoint with the same behavior as flake8 (flake8helled)
    """
    if argv is None:
        argv = sys.argv[1:]
    exit_code, msg = main(['lint'] + argv)
    if msg:
        print(colored(msg, 'red'))
    sys.exit(exit_code)
