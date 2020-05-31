from pathlib import Path
from typing import List
from flake8.processor import FileProcessor
from ..parsers import PARSERS, PythonParser


class FlakeHellProcessor(FileProcessor):
    def read_lines_from_filename(self) -> List[str]:
        """Read the lines for a file."""
        path = Path(self.filename)
        parser = PARSERS.get(path.suffix, PythonParser)
        return parser.parse(path=path)
