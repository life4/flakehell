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

    TOO_MANY_ARGS = 31


KNOWN_PLUGINS = [
    'flake8-alfred',
    'flake8-annotations-complexity',
    'flake8-bandit',
    'flake8-broken-line',
    'flake8-bugbear',
    'flake8-builtins',
    'flake8-coding',
    'flake8-commas',
    'flake8-comprehensions',
    'flake8-debugger',
    'flake8-django',
    'flake8-docstrings',  # pydocstyle
    'flake8-eradicate',
    'flake8-executable',
    'flake8-isort',
    'flake8-logging-format',
    'flake8-mutable',
    'flake8-pep3101',
    'flake8-pie',
    'flake8-print',
    'flake8-quotes',
    'flake8-rst-docstrings',
    'flake8-scrapy',
    # 'flake8-strict',
    'flake8-string-format',
    'flake8-variables-names',
    'pep8-naming',

    # built-in in flake8
    'pycodestyle',
    'pyflakes',
]
