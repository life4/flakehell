import json
from pathlib import Path
from typing import List
from ._base import BaseParser


class JupyterParser(BaseParser):
    @staticmethod
    def parse(path: Path) -> List[str]:
        lines = []
        with path.open(encoding='utf8') as stream:
            notebook = json.load(stream)
            for cell in notebook['cells']:
                if cell['cell_type'] != 'code':
                    continue
                lines.append('\n')
                lines.append('# In [{}]:\n'.format(cell.get('execution_count', 0)))
                lines.extend(line.rstrip('\n') + '\n' for line in cell['source'])
        return lines
