import re
from collections import defaultdict
from typing import Any, Dict, Iterator

from ._plugin import get_plugin_name


REX_CODE = re.compile(r'^[A-Z]{1,5}[0-9]{0,5}$')

ALIASES = {
    'logging-format': 'G',
}


def get_installed(app) -> Iterator[Dict[str, Any]]:
    plugins_codes = defaultdict(list)

    app.initialize([])
    for check_type, checks in app.check_plugins.to_dictionary().items():
        for check in checks:
            code = check['name']
            code = ALIASES.get(code, code)
            if not REX_CODE.match(code):
                continue
            plugins_codes[(check_type, get_plugin_name(check))].append(code)

    for (check_type, name), codes in plugins_codes.items():
        yield dict(
            type=check_type,
            name=name,
            codes=codes,
        )
