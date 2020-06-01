from pathlib import Path
from types import MappingProxyType
from typing import List, Mapping, Tuple


class BaseParser:
    ignore: Mapping[str, Tuple[str, ...]] = MappingProxyType({})

    @staticmethod
    def parse(path: Path) -> List[str]:
        raise NotImplementedError
