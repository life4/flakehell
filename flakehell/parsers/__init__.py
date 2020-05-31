from types import MappingProxyType
from typing import Mapping, Type

from ._base import BaseParser
from ._jupyter import JupyterParser
from ._markdown import MarkdownParser
from ._python import PythonParser


__all__ = ['PARSERS', 'JupyterParser', 'MarkdownParser', 'PythonParser']


PARSERS: Mapping[str, Type[BaseParser]] = MappingProxyType({
    '.ipynb': JupyterParser,
    '.md': MarkdownParser,
    '.py': PythonParser,
})
