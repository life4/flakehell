from pathlib import Path

import pytest

from flakehell._logic import YesQA


def get_modified(content: str, path: Path) -> str:
    path = path / 'tmp.py'
    path.touch()
    return YesQA().get_modified_file(path=path, original=content)


@pytest.mark.parametrize('content', [
    'print("hello")',
    'err=1 # noqa: E225',
    'err=1 # NoQA: E225',
    # 'err="# noqa: E117"',
])
def test_not_modified(content: str, tmp_path: Path):
    assert get_modified(content=content, path=tmp_path) == content


@pytest.mark.parametrize('given, expected', [
    # remove one code
    ('err=1 # noqa: E225, E117', 'err=1 # noqa: E225'),
    ('err=1 # noqa: E117, E225', 'err=1 # noqa: E225'),
    # don't touch text after
    ('err=1 # noqa: E225, E117 # comment', 'err=1 # noqa: E225 # comment'),
    # remove comment when the last code is removed
    ('err=1 # noqa: E117', 'err=1'),
    # case insensitive
    ('err=1 # NoQA: E117', 'err=1'),
])
def test_modified(given: str, expected: str, tmp_path: Path):
    assert get_modified(content=given, path=tmp_path) == expected
