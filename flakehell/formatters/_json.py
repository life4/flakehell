# built-in
import json

# external
from flake8.formatting.base import BaseFormatter


class JSONFormatter(BaseFormatter):
    def format(self, error):
        filename = error.filename
        if filename.startswith('./'):
            filename = filename[2:]
        return json.dumps(dict(
            path=filename,
            code=error.code,
            description=error.text,

            line=error.line_number,
            column=error.column_number,

            context=error.physical_line,
            plugin=getattr(error, 'plugin', None),
        ))
