import re
from typing import Dict, Any


REX_NAME = re.compile(r"[-_.]+")


def get_plugin_name(plugin: Dict[str, Any]) -> str:
    if plugin['plugin_name'] == 'pyflakes':
        return plugin['plugin_name']

    names = (plugin['plugin_name'], plugin['plugin'].__module__)
    names = [REX_NAME.sub('-', name).lower() for name in names]
    for name in names:
        if name.startswith('flake8'):
            return name
    for name in names:
        if name.startswith('pep8'):
            return name
    return names[0]
