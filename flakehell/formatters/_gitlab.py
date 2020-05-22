# built-in
import json

# external
from flake8.formatting.base import BaseFormatter

# app
from .._logic import make_baseline


class GitlabFormatter(BaseFormatter):
    error_format = '{code} {text}'

    def start(self):
        self._write('[')
        self.newline = ''
        self._first_line = True

    def stop(self):
        self._write('\n]\n')

    def handle(self, error):
        # redefined to never output source
        line = self.format(error)
        self._write(line)

    def format(self, error):
        filename = error.filename
        if filename.startswith('./'):
            filename = filename[2:]
        digest = make_baseline(
            path=filename,
            code=error.code,
            line=error.line_number,
            context=error.physical_line,
        )
        text = self.error_format.format(code=error.code, text=error.text)
        # docs.gitlab.com/ee/user/project/merge_requests/code_quality.html
        result = json.dumps(dict(
            description=text,
            fingerprint=digest,
            location={
                'path': filename,
                'lines': dict(begin=error.line_number),
            },
        ))
        if self._first_line:
            self._first_line = False
        else:
            result = ',\n' + result
        return result
