from pathlib import Path
from flakehell._logic import get_exceptions


def test_get_exceptions(tmp_path: Path):
    tests_path = tmp_path / 'tests'
    tests_path.mkdir()
    test_path = tests_path / 'test_example.py'
    test_path.touch()
    source_path = tmp_path / 'example.py'
    source_path.touch()

    exceptions = {
        'tests/': {'pyflakes': ['+*']},
    }
    result = get_exceptions(path=test_path, exceptions=exceptions, root=tmp_path)
    assert result == {'pyflakes': ['+*']}
    result = get_exceptions(path=source_path, exceptions=exceptions, root=tmp_path)
    assert result == {}
