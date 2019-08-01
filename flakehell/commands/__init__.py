from types import MappingProxyType

from ._installed import installed_command
from ._lint import lint_command
from ._show import show_command


__all__ = [
    'COMMANDS',
    'installed_command',
    'lint_command',
    'show_command',
]


COMMANDS = MappingProxyType(dict(
    installed=installed_command,
    lint=lint_command,
    show=show_command,
))
