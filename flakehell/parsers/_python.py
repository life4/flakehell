import tokenize
from pathlib import Path
from types import MappingProxyType
from typing import List, Mapping, Tuple
from ._base import BaseParser


class PythonParser(BaseParser):
    extensions = frozenset({'.py'})
    ignore: Mapping[str, Tuple[str, ...]] = MappingProxyType({})

    @staticmethod
    def parse(path: Path) -> List[str]:
        try:
            with tokenize.open(str(path)) as fd:
                return fd.readlines()
        except (SyntaxError, UnicodeError):
            with open(str(path), encoding='utf8') as fd:
                return fd.readlines()
