import sys
from logging import getLogger
from typing import List, NoReturn

from ._app import FlakeHellApplication
from ._discover import discover
from ._extractors import extract


NAME = 'flakehell'
logger = getLogger(NAME)


def lint_command(argv) -> NoReturn:
    app = FlakeHellApplication(program=NAME, version='1.0.0')
    app.run(argv[1:])
    app.exit()


def installed_command(argv) -> NoReturn:
    app = FlakeHellApplication(program=NAME, version='1.0.0')
    plugins = sorted(discover(app=app), key=lambda p: p['name'])
    if not plugins:
        logger.error('no plugins installed')
        exit(11)
    width = max(len(p['name']) for p in plugins)
    for plugin in plugins:
        print('{} | {}'.format(plugin['name'].ljust(width), ', '.join(plugin['codes'])))
    sys.exit(0)


def show_command(argv) -> NoReturn:
    if not argv:
        logger.error('no plugin name provided')
        exit(21)
    try:
        codes = extract(argv[0])
    except ImportError as e:
        logger.error('cannot import module: {}'.format(e.args[0]))
        exit(22)
    if not codes:
        logger.error('no codes found')
        exit(23)
    width = max(len(code) for code in codes)
    for code, info in sorted(codes.items()):
        print('{} | {}'.format(code.ljust(width), info))
    sys.exit(0)


commands = dict(
    lint=lint_command,
    installed=installed_command,
    show=show_command,
)


def main(argv: List[str] = None) -> NoReturn:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        logger.error('No command provided. Available: {}.'.format(', '.join(sorted(commands))))
        sys.exit(1)
    command_name = argv[0]
    if command_name not in commands:
        logger.error('Invalid command: {}. Available: {}.'.format(
            command_name,
            ', '.join(sorted(commands)),
        ))
        sys.exit(2)
    commands[command_name](argv=argv[1:])
