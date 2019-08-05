import re
from collections import defaultdict
from typing import Any, Dict, Iterator

from ._plugin import get_plugin_name


REX_CODE = re.compile(r'^[A-Z]{1,5}[0-9]{0,5}$')

ALIASES = {
    'logging-format': ('G', ),
    'flake-mutable': ('M511', ),
    'flake8-bandit': ('S', ),
    'pycodestyle': ('W', 'E'),
}


def get_installed(app) -> Iterator[Dict[str, Any]]:
    plugins_codes = defaultdict(list)

    app.initialize([])
    for check_type, checks in app.check_plugins.to_dictionary().items():
        for check in checks:
            key = (check_type, get_plugin_name(check))

            # if codes for plugin specified explicitly in ALIASES, use it
            codes = ALIASES.get(check['plugin_name'])
            if codes:
                plugins_codes[key] = list(codes)
                continue

            # otherwise get codes from plugin entrypoint
            code = check['name']
            if not REX_CODE.match(code):
                raise ValueError('Invalid code format: {}'.format(code))
            plugins_codes[key].append(code)

    for (check_type, name), codes in plugins_codes.items():
        yield dict(
            type=check_type,
            name=name,
            codes=sorted(codes),
        )
