# built-in
from pathlib import Path
from typing import List, Type

# external
from flake8.processor import FileProcessor

# app
from ..parsers import PARSERS, BaseParser, PythonParser


class FlakeHellProcessor(FileProcessor):
    parser: Type[BaseParser] = PythonParser

    def read_lines_from_filename(self) -> List[str]:
        """Read the lines for a file."""
        path = Path(self.filename)
        self.parser = PARSERS.get(path.suffix, PythonParser)
        return self.parser.parse(path=path)
