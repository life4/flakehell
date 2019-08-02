from types import MappingProxyType

from ._excluded import excluded_command
from ._installed import installed_command
from ._lint import lint_command
from ._missed import missed_command
from ._show import show_command
from ._used import used_command


__all__ = [
    'COMMANDS',
    'excluded_command',
    'installed_command',
    'lint_command',
    'show_command',
    'used_command',
]


COMMANDS = MappingProxyType(dict(
    excluded=excluded_command,
    installed=installed_command,
    lint=lint_command,
    missed=missed_command,
    show=show_command,
    used=used_command,
))
