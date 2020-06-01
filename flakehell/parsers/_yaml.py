from pathlib import Path
from types import MappingProxyType
from typing import List
from ._base import BaseParser


class YAMLParser(BaseParser):
    ignore = MappingProxyType({
        'pycodestyle': (),
    })

    @classmethod
    def parse(cls, path: Path) -> List[str]:
        if not path.name.startswith(('test-', 'test_')):
            return []
        try:
            import yaml
        except ImportError:
            return []

        with path.open(encoding='utf8') as stream:
            cases = yaml.safe_load(stream)
        return cls._pytest_mypy_plugins(cases)

    @staticmethod
    def _pytest_mypy_plugins(cases) -> List[str]:
        """Parse pytest-mypy-plugins tests

        https://github.com/typeddjango/pytest-mypy-plugins
        """
        if not isinstance(cases, list):
            return []
        lines = []
        for case in cases:
            if 'case' not in case:
                continue
            if 'main' not in case:
                continue
            lines.append('\n')
            lines.extend(line + '\n' for line in case['main'].splitlines())
        return lines
