# built-in
from pathlib import Path

# app
from .._constants import ExitCode
from .._logic import YesQA
from .._types import CommandResult


def get_paths(paths):
    for path in paths:
        if path.is_dir():
            yield from get_paths(path.iterdir())
            continue
        if path.suffix != '.py':
            continue
        if not path.is_file():
            continue
        yield path


def yesqa_command(argv) -> CommandResult:
    """Remove bare and unused noqa comments.
    """
    if not argv:
        return ExitCode.NOT_ENOUGH_ARGS, 'no file path provided'
    if argv[0] == '--help':
        print(yesqa_command.__doc__)
        return ExitCode.OK, ''

    paths = get_paths(Path(fname) for fname in argv)
    fixer = YesQA()
    for path in paths:
        modified = fixer(path=path)
        if modified:
            print(str(path))
    return ExitCode.OK, ''
