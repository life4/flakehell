from .._app import FlakeHellApplication
from .._constants import NAME, VERSION, ExitCodes
from .._discover import get_installed
from .._types import CommandResult


def installed_command(argv) -> CommandResult:
    app = FlakeHellApplication(program=NAME, version=VERSION)
    plugins = sorted(get_installed(app=app), key=lambda p: p['name'])
    if not plugins:
        return ExitCodes.NO_PLUGINS_INSTALLED, 'no plugins installed'
    width = max(len(p['name']) for p in plugins)
    for plugin in plugins:
        print('{} | {}'.format(plugin['name'].ljust(width), ', '.join(plugin['codes'])))
    return 0, ''
