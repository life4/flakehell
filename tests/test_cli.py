import subprocess
import sys


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
