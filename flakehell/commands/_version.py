from termcolor import colored

from .._types import CommandResult
from .._version import __version__ as flakehell_version
from flake8 import __version__ as flake8_version


def version_command(argv) -> CommandResult:
    """Show FlakeHell version.
    """
    print('FlakeHell', colored(flakehell_version, 'green'))
    print('Flake8   ', colored(flake8_version, 'green'))
    print('For plugins versions use', colored('flakehell plugins', 'green'))
    return 0, ''
