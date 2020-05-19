import subprocess
import os
import sys
from contextlib import contextmanager
from pathlib import Path
from textwrap import dedent

import pytest
from flakehell._cli import main


@contextmanager
def chdir(path):
    """Context manager for changing dir and restoring previous workdir after exit.
    """
    curdir = os.getcwd()
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(curdir)


def test_flake8helled_file():
    """Baseline behavior, when an actual filename is passed."""
    cmd = [
        sys.executable,
        '-c',
        'import sys; from flakehell import flake8_entrypoint; sys.exit(flake8_entrypoint())',
        __file__,
    ]
    result = subprocess.run(cmd)
    assert result.returncode == 0


def test_flake8helled_stdin():
    """Problematic behavior from issue #44, `-` is passed as filename, together with --stdin-display-name."""
    source_file = open(__file__, 'r')
    cmd = [
        sys.executable,
        '-c',
        'import sys; from flakehell import flake8_entrypoint; sys.exit(flake8_entrypoint())',
        '--stdin-display-name',
        __file__,
        # '-' is not an existing filename, so snapshot cannot create a hexdigest of its content
        # but otherwise it's fine for flake8 which knows to read stdin instead
        '-',
    ]
    result = subprocess.run(cmd, stdin=source_file)
    assert result.returncode == 0


@pytest.mark.parametrize('flag', [
    '--help',
    'help',
    'commands',
])
def test_help(flag, capsys):
    result = main([flag])
    assert result == (0, '')
    captured = capsys.readouterr()
    assert captured.err == ''

    for name in ('baseline', 'code', 'codes', 'lint', 'missed', 'plugins'):
        assert name in captured.out


def test_lint_help(capsys):
    result = main(['lint', '--help'])
    assert result == (0, '')
    captured = capsys.readouterr()
    assert captured.err == ''
    assert '-h, --help' in captured.out
    assert '--builtins' in captured.out
    assert '--isort-show-traceback' in captured.out


def test_exclude(capsys, tmp_path: Path):
    text = """
    [tool.flakehell.plugins]
    pyflakes = ["+*"]

    [tool.flakehell.exceptions."tests/"]
    pyflakes = ["-F401"]
    """
    (tmp_path / 'pyproject.toml').write_text(dedent(text))
    (tmp_path / 'example.py').write_text('import sys\na')
    (tmp_path / 'tests').mkdir()
    (tmp_path / 'tests' / 'test_example.py').write_text('import sys\na')
    with chdir(tmp_path):
        result = main(['lint', '--format', 'default'])
    assert result == (1, '')
    captured = capsys.readouterr()
    assert captured.err == ''
    exp = """
    ./example.py:1:1: F401 'sys' imported but unused
    ./example.py:2:1: F821 undefined name 'a'
    ./tests/test_example.py:2:1: F821 undefined name 'a'
    """
    assert captured.out.strip() == dedent(exp).strip()
