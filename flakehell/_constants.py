from colorama import Fore
from enum import IntEnum


NAME = 'flakehell'
VERSION = '0.1.0'


class ExitCodes(IntEnum):
    # CLI entrypoint
    NO_COMMAND = 1
    INVALID_COMMAND = 2

    # `installed` command
    NO_PLUGINS_INSTALLED = 11

    # `show` command
    NO_PLUGIN_NAME = 21
    IMPORT_ERROR = 22
    NO_CODES = 23


COLORS = dict(
    W=Fore.YELLOW,
    E=Fore.RED,
    WPS=Fore.MAGENTA,
    default=Fore.GREEN,
)
