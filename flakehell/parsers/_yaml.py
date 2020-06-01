from pathlib import Path
from types import MappingProxyType
from typing import List
from ._base import BaseParser


class YAMLParser(BaseParser):
    ignore = MappingProxyType({
        'pycodestyle': ('E302', 'E303', 'E305', 'E402', 'E501', 'W391'),
    })

    @classmethod
    def parse(cls, path: Path) -> List[str]:
        if not path.name.startswith(('test-', 'test_')):
            return []
        with path.open(encoding='utf8') as stream:
            return cls._pytest_mypy_plugins(stream)

    @staticmethod
    def _pytest_mypy_plugins(stream) -> List[str]:
        """Parse pytest-mypy-plugins tests

        https://github.com/typeddjango/pytest-mypy-plugins
        """
        code_block = False
        code_found = False
        indent = True
        lines = []
        for line in stream:
            if not line.strip():
                lines.append('\n')
                continue

            # start of new case or another directive inside the current case
            current_indent = len(line) - len(line.lstrip())
            if indent is not None and current_indent < indent:
                code_block = False
                lines.append('# ' + line)
                continue

            # start of code block
            if line.lstrip().startswith('main: |'):
                code_block = True
                indent = None
                lines.append('# ' + line)
                continue

            if indent is None:
                indent = current_indent
            if code_block:
                lines.append(line[indent:])
                code_found = True
        if not code_found:
            return []
        lines[0] = 'reveal_type = lambda x: x  # noqa\n'
        return lines
