from pathlib import Path
from typing import List


class BaseParser:
    @staticmethod
    def parse(path: Path) -> List[str]:
        raise NotImplementedError
