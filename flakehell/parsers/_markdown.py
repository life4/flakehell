from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Optional
from typing import List
from ._base import BaseParser


class CodeType(Enum):
    PYTHON = 'python'
    PYCON = 'pycon'


class MarkdownParser(BaseParser):
    ignore = MappingProxyType({
        'pycodestyle': (),
    })

    @classmethod
    def parse(cls, path: Path) -> List[str]:
        code_found = False
        code_type = None
        indent = None
        lines = []
        with path.open('r', encoding='utf8') as stream:
            for line in stream:
                # leave empty lines as-is
                if not line.strip():
                    lines.append('\n')
                    continue

                if code_type is None:
                    # detect code block start
                    new_code_type = cls._get_code_type(line=line)
                    if new_code_type:
                        code_type = new_code_type
                    # ignore markdown and code block starts
                    lines.append('# <removed>\n')
                    continue

                # detect code block end
                if line.strip() == '```':
                    code_type = None
                    lines.append('# <removed>\n')
                    indent = None
                    continue

                # For the first line of code check indentation.
                if indent is None:
                    indent = len(line) - len(line.lstrip())
                # Remove this identation from every line of the code block
                line = line[indent:]

                # remove repl chars and comment-out output
                if code_type == CodeType.PYCON:
                    if line.startswith('>>> ') or line.startswith('... '):
                        line = line[4:]
                    else:
                        line = '# ' + line

                # save code line as-is
                lines.append(line)
                code_found = True
        if not code_found:
            return []
        return lines

    @staticmethod
    def _get_code_type(line: str) -> Optional[CodeType]:
        line = line.lstrip()
        if line[:3] != '```':
            return None
        line = line[3:]
        for tp in CodeType:
            if line.lower().startswith(tp.value):
                return tp
        return None
