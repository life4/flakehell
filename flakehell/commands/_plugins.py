from termcolor import colored

from .._constants import NAME, VERSION, ExitCodes
from .._logic import get_installed, get_plugin_rules
from .._patched import FlakeHellApplication
from .._types import CommandResult


def plugins_command(argv) -> CommandResult:
    """Show all installed plugins, their codes prefix, and matched rules from config.
    """
    app = FlakeHellApplication(program=NAME, version=VERSION)
    plugins = sorted(get_installed(app=app), key=lambda p: p['name'])
    if not plugins:
        return ExitCodes.NO_PLUGINS_INSTALLED, 'no plugins installed'

    width = max(len(p['name']) for p in plugins)
    template = '{name} | {codes:8} | {rules}'
    print(template.format(
        name=colored('NAME'.ljust(width), 'yellow'),
        codes=colored('CODES   ', 'yellow'),
        rules=colored('RULES', 'yellow'),
    ))
    showed = set()
    for plugin in plugins:
        # Plugins returned by get_installed are unique by namee and type.
        # We are not showing type, so, let's show one name only once.
        if plugin['name'] in showed:
            continue
        showed.add(plugin['name'])

        rules = get_plugin_rules(
            plugin_name=plugin['name'],
            plugins=app.options.plugins,
        )
        colored_rules = []
        for rule in rules:
            if rule[0] == '+':
                rule = colored(rule, 'green')
            elif rule[0] == '-':
                rule = colored(rule, 'red')
            colored_rules.append(rule)
        color = 'green' if rules else 'red'
        print(template.format(
            name=colored(plugin['name'].ljust(width), color),
            codes=', '.join(plugin['codes']),
            rules=', '.join(colored_rules),
        ))
    return 0, ''
