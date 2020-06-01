from pathlib import Path
from types import MappingProxyType
from typing import List, Optional
from ._base import BaseParser
from ._markdown import CODE_TYPES, CodeType


class RSTParser(BaseParser):
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
                        indent = None
                    # ignore rst and code block starts
                    lines.append('# {}\n'.format(line[:40].strip()))
                    continue

                # detect code block end
                current_indent = len(line) - len(line.lstrip())
                if indent is not None and current_indent < indent:
                    code_type = None
                    lines.append('# {}\n'.format(line[:40].strip()))
                    continue

                # For the first line of code check indentation.
                if indent is None:
                    indent = current_indent
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
        if line[:2] != '..':
            return None
        line = line[2:].lstrip()
        block, sep, lang = line.partition('::')
        if not sep:
            return None
        if block.strip() not in ('code-block', 'code', 'sourcecode', 'ipython'):
            return None
        lang = lang.strip().lower()
        return CODE_TYPES.get(lang, None)
