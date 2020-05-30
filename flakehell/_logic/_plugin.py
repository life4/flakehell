# built-in
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

# external
from flake8.utils import fnmatch


REX_NAME = re.compile(r'[-_.]+')
ALIASES = {
    'flake-mutable': 'flake8-mutable',
    'pyflakes': 'pyflakes',
    'naming': 'pep8-naming',
    'logging-format': 'flake8-logging-format',
}
PluginsType = Dict[str, List[str]]


def get_plugin_name(plugin: Dict[str, Any]) -> str:
    """Get plugin name from plugin info

    Users expect the same plugin name as the name of the package that provides plugin.
    However, that's not true for some plugins.
    Also, some plugins has different module name, that doesn't match to package.

    Lookup order:

    1. Ad-hoc aliases when nothing match
    2. Normalized name that starts with `flake8`
    3. Normalized name that starts with `pep`
    4. `plugin_name`
    """
    if not plugin:
        return 'UNKNOWN'
    if plugin['plugin_name'] in ALIASES:
        return ALIASES[plugin['plugin_name']]

    names = (plugin['plugin_name'], plugin['plugin'].__module__)
    names = [REX_NAME.sub('-', name).lower() for name in names]
    for name in names:
        if name.startswith('flake8'):
            return name
    for name in names:
        if name.startswith('pep8'):
            return name
    return names[0]


def get_plugin_rules(plugin_name: str, plugins: PluginsType) -> List[str]:
    """Get rules for plugin from `plugins` in the config

    Plugin name can be specified as a glob expression.
    So, it's not trivial to match the right one

    1. Try to find exact match (normalizing ass all packages names normalized)
    2. Try to find globs that match and select the longest one (nginx-style)
    3. Return empty list if nothing is found.
    """
    if not plugins:
        return []
    plugin_name = REX_NAME.sub('-', plugin_name).lower()
    # try to find exact match
    for pattern, rules in plugins.items():
        if '*' not in pattern and REX_NAME.sub('-', pattern).lower() == plugin_name:
            return rules

    # try to find match by pattern and select the longest
    best_match = (0, [])  # type: Tuple[int, List[str]]
    for pattern, rules in plugins.items():
        if not fnmatch(filename=plugin_name, patterns=[pattern]):
            continue
        match = len(pattern)
        if match > best_match[0]:
            best_match = match, rules
    if best_match[0]:
        return best_match[1]

    return []


def check_include(code: str, rules: List[str]) -> bool:
    """
    0. Validate rules

    1. Return True if rule explicitly included
    2. Return False if rule explicitly excluded

    3. Return True if the latest glob-matching rule is include
    4. Return False if the latest glob-matching rule is exclude
    """
    # always report exceptions in file processing
    if code in ('E902', 'E999'):
        return True

    for rule in rules:
        if len(rule) < 2 or rule[0] not in {'-', '+'}:
            raise ValueError('invalid rule: `{}`'.format(rule))

    for rule in reversed(rules):
        if code.lower() == rule[1:].lower():
            return rule[0] == '+'

    include = False
    for rule in rules:
        if fnmatch(code, patterns=[rule[1:]]):
            include = rule[0] == '+'
    return include


def get_exceptions(
    path: Union[str, Path], exceptions: Dict[str, PluginsType], root: Path = None,
) -> PluginsType:
    if not exceptions:
        return dict()
    if isinstance(path, str):
        path = Path(path)
    if root is None:
        root = Path().resolve()
    path = path.resolve().relative_to(root).as_posix()
    exceptions = sorted(
        exceptions.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    )

    # prefix
    for path_rule, rules in exceptions:
        if '*' in path_rule:
            continue
        if path.startswith(path_rule):
            return rules

    # glob
    for path_rule, rules in exceptions:
        if '*' not in path_rule:
            continue
        if fnmatch(filename=path, patterns=[path_rule]):
            return rules

    return dict()
