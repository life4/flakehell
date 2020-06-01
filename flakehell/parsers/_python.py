import tokenize
from pathlib import Path
from typing import List
from ._base import BaseParser


class PythonParser(BaseParser):
    @staticmethod
    def parse(path: Path) -> List[str]:
        try:
            with tokenize.open(str(path)) as fd:
                return fd.readlines()
        except (SyntaxError, UnicodeError):
            with open(str(path), encoding='utf8') as fd:
                return fd.readlines()
