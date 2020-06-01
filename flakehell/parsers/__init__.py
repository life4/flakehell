from types import MappingProxyType
from typing import Mapping, Type

from ._base import BaseParser
from ._jupyter import JupyterParser
from ._markdown import MarkdownParser
from ._python import PythonParser
from ._yaml import YAMLParser


__all__ = [
    'BaseParser',
    'JupyterParser',
    'MarkdownParser',
    'PARSERS',
    'PythonParser',
    'YAMLParser',
]


PARSERS: Mapping[str, Type[BaseParser]] = MappingProxyType({
    '.ipynb': JupyterParser,
    '.md': MarkdownParser,
    '.py': PythonParser,
    '.yaml': YAMLParser,
    '.yml': YAMLParser,
})
