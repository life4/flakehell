from types import MappingProxyType

from ._jupyter import JupyterParser
from ._markdown import MarkdownParser
from ._python import PythonParser


__all__ = ['PARSERS', 'JupyterParser', 'MarkdownParser', 'PythonParser']


PARSERS = MappingProxyType({
    '.ipynb': JupyterParser,
    '.md': MarkdownParser,
    '.py': PythonParser,
})
