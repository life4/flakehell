# built-in
from pathlib import Path

# project
from flakehell._logic import get_exceptions


def test_get_exceptions(tmp_path: Path):
    exceptions = {
        'tests/': {'pyflakes': ['+*']},
        'test_*.py': {'pycodestyle': ['+*']},
    }

    # prefix match
    tests_path = tmp_path / 'tests'
    tests_path.mkdir()
    test_path = tests_path / 'test_example.py'
    test_path.touch()
    result = get_exceptions(path=test_path, exceptions=exceptions, root=tmp_path)
    assert result == {'pyflakes': ['+*']}

    # glob match
    base_test_path = tmp_path / 'test_example.py'
    base_test_path.touch()
    result = get_exceptions(path=base_test_path, exceptions=exceptions, root=tmp_path)
    assert result == {'pycodestyle': ['+*']}

    # no match
    source_path = tmp_path / 'example.py'
    source_path.touch()
    result = get_exceptions(path=source_path, exceptions=exceptions, root=tmp_path)
    assert result == {}
