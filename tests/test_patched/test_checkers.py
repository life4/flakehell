# built-in
from unittest import mock

# project
from flakehell._patched._checkers import FlakeHellFileChecker


def test_nonexistent_file():
    """Verify that checking non-existent file results in an error."""
    plugin = {
        'plugin_name': 'flake8-example',
        'name': 'something',
        'plugin': FlakeHellFileChecker,
    }
    checks = dict(ast_plugins=[plugin], logical_line_plugins=[], physical_line_plugins=[])
    c = FlakeHellFileChecker(
        filename='foobar.py',
        checks=checks,
        options=None,
    )

    assert c.processor is None
    assert not c.should_process
    assert len(c.results) == 1
    error = c.results[0]
    assert error.error_code == 'E902'


def test_catches_exception_on_invalid_syntax(tmp_path):
    code_path = tmp_path / 'example.py'
    code_path.write_text('I exist!')
    plugin = {
        'name': 'failure',
        'plugin_name': 'failure',
        'parameters': dict(),
        'plugin': mock.MagicMock(side_effect=ValueError),
    }
    options = mock.MagicMock()
    options.safe = False
    checks = dict(ast_plugins=[plugin], logical_line_plugins=[], physical_line_plugins=[])
    fchecker = FlakeHellFileChecker(
        filename=str(code_path),
        checks=checks,
        options=options,
    )
    assert fchecker.should_process is True
    assert fchecker.processor is not None
    fchecker.run_checks()
    assert len(fchecker.results) == 1
    assert fchecker.results[0].error_code == 'E999'
    assert fchecker.results[0].text == 'SyntaxError: invalid syntax'
