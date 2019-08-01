from .._app import FlakeHellApplication
from .._constants import NAME, VERSION
from .._types import CommandResult


def lint_command(argv) -> CommandResult:
    app = FlakeHellApplication(program=NAME, version=VERSION)
    try:
        app.run(argv)
        app.exit()
    except SystemExit as exc:
        return exc.code, ''
