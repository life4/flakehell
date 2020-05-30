# app
from .._constants import NAME, VERSION, ExitCode
from .._logic import get_installed, get_plugin_rules
from .._patched import FlakeHellApplication
from .._types import CommandResult


def missed_command(argv) -> CommandResult:
    """Show patterns from the config that has no matched plugin installed.
    """
    if argv and argv[0] == '--help':
        print(missed_command.__doc__)
        return ExitCode.OK, ''
    if argv:
        return ExitCode.TOO_MANY_ARGS, 'the command does not accept arguments'

    app = FlakeHellApplication(program=NAME, version=VERSION)
    installed_plugins = sorted(get_installed(app=app), key=lambda p: p['name'])
    if not installed_plugins:
        return ExitCode.NO_PLUGINS_INSTALLED, 'no plugins installed'

    count = 0
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
            count += 1
    return count, ''
