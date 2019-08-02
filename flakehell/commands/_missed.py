from .._constants import NAME, VERSION, ExitCodes
from .._logic import get_installed, get_plugin_rules
from .._patched import FlakeHellApplication
from .._types import CommandResult


def missed_command(argv) -> CommandResult:
    app = FlakeHellApplication(program=NAME, version=VERSION)
    installed_plugins = sorted(get_installed(app=app), key=lambda p: p['name'])
    if not installed_plugins:
        return ExitCodes.NO_PLUGINS_INSTALLED, 'no plugins installed'
    for pattern in app.options.plugins:
        for plugin in installed_plugins:
            rules = get_plugin_rules(
                plugin_name=plugin['name'],
                plugins={pattern: ['+*']},
            )
            if rules:
                break
        else:
            print(pattern)
    return 0, ''
