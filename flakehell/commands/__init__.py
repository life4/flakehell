from types import MappingProxyType

from ._plugins import plugins_command
from ._lint import lint_command
from ._missed import missed_command
from ._codes import codes_command


__all__ = [
    'COMMANDS',
    'lint_command',
    'plugins_command',
    'show_command',
]


COMMANDS = MappingProxyType(dict(
    codes=codes_command,
    lint=lint_command,
    missed=missed_command,
    plugins=plugins_command,
))
