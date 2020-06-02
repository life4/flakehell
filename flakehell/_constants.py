# built-in
from types import MappingProxyType
from enum import IntEnum

# app
from ._version import __version__


NAME = 'flakehell'
VERSION = __version__


# our own modern defaults
DEFAULTS = dict(
    # redefined defaults
    filename=['*.py', '*.ipynb', '*.md', '*.yml', '*.yaml', '*.rst', '*.rest'],
    format='colored',
    max_line_length=90,

    # flakehell options
    baseline=None,
    safe=False,
    plugins={
        'pyflakes': ['+*'],
        'pycodestyle': ['+*'],
    },
    exceptions={},

    # disabled by flakehell but required by flake8
    extend_exclude=[],
    ignore=[],
    extend_ignore=[],
    select=[],
    enable_extensions=[],
    per_file_ignores=[],
    statistics=False,
)


class ExitCode(IntEnum):
    OK = 0

    # CLI entrypoint
    NO_COMMAND = 1
    INVALID_COMMAND = 2

    # `installed` command
    NO_PLUGINS_INSTALLED = 11

    # `show` command
    NO_PLUGIN_NAME = 21
    IMPORT_ERROR = 22
    NO_CODES = 23

    TOO_MANY_ARGS = 31
    NOT_ENOUGH_ARGS = 32


KNOWN_PLUGINS = MappingProxyType({
    'dlint': '',
    'flake8-2020': 'https://github.com/asottile/flake8-2020',
    'flake8-alfred': 'https://github.com/datatheorem/flake8-alfred',
    'flake8-annotations-complexity': '',
    'flake8-bandit': '',
    'flake8-black': 'https://github.com/peterjc/flake8-black',
    'flake8-broken-line': 'https://github.com/sobolevn/flake8-broken-line',
    'flake8-bugbear': 'https://github.com/PyCQA/flake8-bugbear',
    'flake8-builtins': 'https://github.com/gforcada/flake8-builtins',
    'flake8-coding': 'https://github.com/tk0miya/flake8-coding',
    'flake8-commas': 'https://github.com/PyCQA/flake8-commas',
    'flake8-comprehensions': 'https://github.com/adamchainz/flake8-comprehensions',
    'flake8-debugger': 'https://github.com/JBKahn/flake8-debugger',
    'flake8-django': 'https://github.com/rocioar/flake8-django',
    'flake8-docstrings': '',  # pydocstyle
    'flake8-eradicate': 'https://github.com/sobolevn/flake8-eradicate',
    'flake8-executable': 'https://github.com/xuhdev/flake8-executable',
    'flake8-fixme': 'https://github.com/tommilligan/flake8-fixme',
    'flake8-future-import': '',
    'flake8-isort': '',
    'flake8-logging-format': 'https://github.com/globality-corp/flake8-logging-format',
    'flake8-mutable': 'https://github.com/ebeweber/flake8-mutable',
    'flake8-mypy': 'https://github.com/ambv/flake8-mypy',
    'flake8-pep3101': 'https://github.com/gforcada/flake8-pep3101',
    'flake8-pie': 'https://github.com/sbdchd/flake8-pie',
    'flake8-print': 'https://github.com/JBKahn/flake8-print',
    'flake8-printf-formatting': 'https://github.com/atugushev/flake8-printf-formatting',
    'flake8-pyi': 'https://github.com/ambv/flake8-pyi',
    'flake8-pytest-style': 'https://github.com/m-burst/flake8-pytest-style',
    'flake8-pytest': '',
    'flake8-requirements': 'https://github.com/Arkq/flake8-requirements',
    'flake8-quotes': 'https://github.com/zheller/flake8-quotes',
    'flake8-rst-docstrings': '',
    'flake8-scrapy': 'https://github.com/stummjr/flake8-scrapy',
    'flake8-strict': 'https://github.com/smarkets/flake8-strict',
    'flake8-string-format': 'https://github.com/xZise/flake8-string-format',
    'flake8-variables-names': 'https://github.com/best-doctor/flake8-variables-names',
    'mccabe': '',
    'pep8-naming': '',
    'pylint': '',

    # built-in in flake8
    'pycodestyle': '',
    'pyflakes': '',
})
