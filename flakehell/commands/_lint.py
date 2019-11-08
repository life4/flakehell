
from .._constants import NAME, VERSION
from .._logging import configure_logging
from .._patched import FlakeHellApplication
from .._types import CommandResult


def lint_command(argv) -> CommandResult:
    """Run patched flake8 against the code.
    """
    configure_logging()
    app = FlakeHellApplication(program=NAME, version=VERSION)
    try:
        app.run(argv)
        app.exit()
    except SystemExit as exc:
        return exc.code, ''
