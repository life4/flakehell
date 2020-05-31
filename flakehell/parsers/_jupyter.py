import json
from pathlib import Path
from types import MappingProxyType


class JupyterParser:
    extensions = frozenset({'.ipynb'})
    ignore = MappingProxyType({
        'pycodestyle': (),
    })

    @staticmethod
    def parse(path: Path) -> str:
        lines = []
        with path.open('r', encoding='utf8') as stream:
            notebook = json.load(stream)
            for cell in notebook['cells']:
                if cell['cell_type'] != 'code':
                    continue
                lines.append('\n# In [{}]:'.format(cell.get('execution_count', 0)))
                lines.extend(line.rstrip('\n') for line in cell['source'])
        return '\n'.join(lines) + '\n'
