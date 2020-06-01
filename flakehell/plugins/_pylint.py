# built-in
from ast import AST
from tokenize import TokenInfo
from typing import Sequence

# external
from pylint.__pkginfo__ import version
from pylint.lint import Run
from pylint.reporters import BaseReporter


STDIN = 'stdin'


class Reporter(BaseReporter):
    def __init__(self):
        self.errors = []
        super().__init__()

    def _display(self, layout):
        pass

    def handle_message(self, msg):
        # ignore `invalid syntax` messages, it is already checked by `pycodestyle`
        if msg.msg_id == 'E0001':
            return
        self.errors.append(dict(
            row=msg.line,
            col=msg.column,
            text='{} {}'.format(msg.msg_id, msg.msg or ''),
            code=msg.msg_id,
        ))


class PyLintChecker:
    name = 'pylint'
    version = version

    def __init__(self, tree: AST, file_tokens: Sequence[TokenInfo], filename: str = STDIN) -> None:
        self.tree = tree
        self.filename = filename
        self.file_tokens = file_tokens

    def run(self):
        reporter = Reporter()
        Run([self.filename], reporter=reporter, do_exit=False)
        for error in reporter.errors:
            yield error['row'], error['col'], error['text'], type(self)
