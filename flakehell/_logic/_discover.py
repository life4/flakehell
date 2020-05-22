# built-in
import re
from collections import defaultdict
from typing import Any, Dict, Iterator, Iterable

# app
from ._plugin import get_plugin_name


REX_CODE = re.compile(r'^[A-Z]{1,5}[0-9]{0,5}$')

ALIASES = {
    'flake-mutable': ('M511', ),
    'flake8-bandit': ('S', ),
    'flake8-django': ('DJ', ),  # they say `DJ0` prefix but codes have `DJ10`
    'flake8-future-import': ('FI', ),
    'flake8-mock': ('M001', ),
    'flake8-pytest': ('T003', ),
    'logging-format': ('G', ),
    'pycodestyle': ('W', 'E'),
    'pylint': ('C', 'E', 'F', 'I', 'R', 'W'),
}


def get_installed(app) -> Iterator[Dict[str, Any]]:
    plugins_codes = defaultdict(list)
    versions = dict()

    app.initialize([])
    codes: Iterable[str]

    for check_type in ('ast_plugins', 'logical_line_plugins', 'physical_line_plugins'):
        for plugin in getattr(app.check_plugins, check_type):
            key = (check_type, get_plugin_name(plugin.to_dictionary()))
            versions[key[-1]] = plugin.version

            # if codes for plugin specified explicitly in ALIASES, use it
            codes = ALIASES.get(plugin.plugin_name, [])
            if codes:
                plugins_codes[key] = list(codes)
                continue

            # otherwise get codes from plugin entrypoint
            code = plugin.name
            if not REX_CODE.match(code):
                raise ValueError('Invalid code format: {}'.format(code))
            plugins_codes[key].append(code)

    if 'flake8-docstrings' in versions:
        versions['flake8-docstrings'] = versions['flake8-docstrings'].split(',')[0]

    for (check_type, name), codes in plugins_codes.items():
        yield dict(
            type=check_type,
            name=name,
            codes=sorted(codes),
            version=versions[name],
        )
