from termcolor import colored

from .._constants import NAME, VERSION, ExitCodes
from .._logic import get_installed, color_description, extract
from .._patched import FlakeHellApplication
from .._types import CommandResult


def code_command(argv) -> CommandResult:
    """Show plugin name and message for given code.
    """
    if not argv:
        return ExitCodes.NO_PLUGIN_NAME, 'no plugin name provided'
    if argv[0] == '--help':
        print(code_command.__doc__)
        return 0, ''
    if len(argv) > 1:
        return ExitCodes.TOO_MANY_ARGS, 'the command accept only one argument'
    code = argv[0]

    app = FlakeHellApplication(program=NAME, version=VERSION)
    plugins = sorted(get_installed(app=app), key=lambda p: p['name'])
    if not plugins:
        return ExitCodes.NO_PLUGINS_INSTALLED, 'no plugins installed'

    messages = []
    checked = set()
    for plugin in plugins:
        if plugin['name'] in checked:
            continue
        checked.add(plugin['name'])
        if not code.startswith(tuple(plugin['codes'])):
            continue
        try:
            codes = extract(plugin['name'])
        except ImportError:
            continue
        if code not in codes:
            continue
        messages.append(dict(
            plugin=plugin['name'],
            message=codes[code],
        ))

    if not messages:
        return ExitCodes.NO_CODES, 'no messages found'

    width = max(len(m['plugin']) for m in messages)
    template = '{plugin} | {message}'
    print(template.format(
        plugin=colored('PLUGIN'.ljust(width), 'yellow'),
        message=colored('MESSAGE', 'yellow'),
    ))
    for message in messages:
        print(template.format(
            plugin=message['plugin'].ljust(width),
            message=color_description(message['message']),
        ))
    return 0, ''
