# built-in
from types import SimpleNamespace

# app
from .._constants import NAME, VERSION
from .._patched import FlakeHellApplication
from .._types import CommandResult
from ..formatters import BaseLineFormatter


def baseline_command(argv) -> CommandResult:
    """Generate baseline that can be used later to ignore errors.
    """
    app = FlakeHellApplication(program=NAME, version=VERSION)
    app.formatter = BaseLineFormatter(SimpleNamespace(
        output_file=None,
        show_source=False,
    ))
    try:
        app.run(['--baseline', '', '--exit-zero'] + argv)
        app.exit()
    except SystemExit as exc:
        return int(exc.code), ''
    raise RuntimeError('unreachable')
