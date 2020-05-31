import tokenize
from pathlib import Path
from types import MappingProxyType
from typing import List


class PythonParser:
    extensions = frozenset({'.py'})
    ignore = MappingProxyType({})

    @staticmethod
    def parse(path: Path) -> List[str]:
        try:
            with tokenize.open(str(path)) as fd:
                return fd.readlines()
        except (SyntaxError, UnicodeError):
            # If we can't detect the codec with tokenize.detect_encoding, or
            # the detected encoding is incorrect, just fallback to latin-1.
            with open(str(path), encoding="latin-1") as fd:
                return fd.readlines()
