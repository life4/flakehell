# built-in
from types import MappingProxyType

# app
from ._baseline import baseline_command
from ._code import code_command
from ._codes import codes_command
from ._lint import lint_command
from ._missed import missed_command
from ._plugins import plugins_command
from ._version import version_command
from ._yesqa import yesqa_command


__all__ = [
    'COMMANDS',

    'baseline_command',
    'code_command',
    'codes_command',
    'lint_command',
    'missed_command',
    'plugins_command',
    'version_command',
    'yesqa_command',
]


COMMANDS = MappingProxyType({
    'baseline': baseline_command,
    'code': code_command,
    'codes': codes_command,
    'lint': lint_command,
    'missed': missed_command,
    'plugins': plugins_command,
    'yesqa': yesqa_command,
    '--version': version_command,
})
