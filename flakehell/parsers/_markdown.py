from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Optional
from typing import List
from ._base import BaseParser


class CodeType(Enum):
    PYTHON = 'python'
    PYCON = 'pycon'


CODE_TYPES = {
    'python': CodeType.PYTHON,
    'python3': CodeType.PYTHON,
    'py3': CodeType.PYTHON,
    'python2': CodeType.PYTHON,
    'py2': CodeType.PYTHON,

    'pycon': CodeType.PYCON,
}


class MarkdownParser(BaseParser):
    ignore = MappingProxyType({
        'pycodestyle': ('E302', 'E303', 'E305', 'E402'),
    })

    @classmethod
    def parse(cls, path: Path) -> List[str]:
        code_found = False
        code_type = None
        indent = None
        lines = []
        with path.open(encoding='utf8') as stream:
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
                    lines.append('# {}\n'.format(line[:40].strip()))
                    continue

                # detect code block end
                if line.strip() == '```':
                    code_type = None
                    lines.append('# {}\n'.format(line[:40].strip()))
                    indent = None
                    continue

                # For the first line of code check indentation.
                if indent is None:
                    indent = len(line) - len(line.lstrip())
                    if line.lstrip()[:4] == '>>> ':
                        code_type = CodeType.PYCON
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
        words = line[3:].lower().split()
        if not words:
            return None
        lang = words[0]
        return CODE_TYPES.get(lang, None)
