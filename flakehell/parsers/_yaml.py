from pathlib import Path
from types import MappingProxyType
from typing import List
from ._base import BaseParser


class YAMLParser(BaseParser):
    ignore = MappingProxyType({
        'pycodestyle': ('E302', 'E303', 'E305', 'E402'),
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
        indent = None
        lines = []
        for line in stream:
            if not line.strip():
                lines.append('\n')
                continue

            if not code_block:
                # start of code block
                if line.lstrip().startswith('main: |'):
                    code_block = True
                    indent = None
                # ignore not code blocks
                lines.append('# ' + line.lstrip())
                continue

            # end of code block
            current_indent = len(line) - len(line.lstrip())
            if indent is not None and current_indent < indent:
                code_block = False
                lines.append('# ' + line.lstrip())
                continue

            # wite line from a code block
            if indent is None:
                indent = current_indent
            lines.append(line[indent:])
            code_found = True

        if not code_found:
            return []
        # Replace the first line (it can't be an actual code) by a mock for `reveal_type`.
        lines[0] = 'reveal_type = lambda x: x  # noqa\n'
        return lines
