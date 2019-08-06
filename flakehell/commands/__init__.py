from types import MappingProxyType

from ._baseline import baseline_command
from ._codes import codes_command
from ._lint import lint_command
from ._missed import missed_command
from ._plugins import plugins_command


__all__ = [
    'COMMANDS',

    'baseline_command',
    'codes_command',
    'lint_command',
    'missed_command',
    'plugins_command',
]


COMMANDS = MappingProxyType(dict(
    baseline=baseline_command,
    codes=codes_command,
    lint=lint_command,
    missed=missed_command,
    plugins=plugins_command,
))
