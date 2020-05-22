# built-in
from pathlib import Path

# external
import pytest

# project
from flakehell._logic import YesQA

# app
from ..utils import chdir


def get_modified(content: str, path: Path) -> str:
    path = path / 'tmp.py'
    path.write_text(content)
    with chdir(path.parent):
        return YesQA().get_modified_file(path=path, original=content)


@pytest.mark.parametrize('content', [
    'print("hello")',
    # don't add not ignored codes
    'err=1',
    # don't touch other codes
    'err=1 # noqa: E225',
    # preserve case
    'err=1 # NoQA: E225',
    # respect tokenization structure
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

    # https://github.com/asottile/yesqa/blob/master/tests/yesqa_test.py
    ('import os  # noqa: F401,X999\n', 'import os  # noqa: F401\n'),
    ('import os  # noqa:F401,X999\n', 'import os  # noqa: F401\n'),
])
def test_modified(given: str, expected: str, tmp_path: Path):
    assert get_modified(content=given, path=tmp_path) == expected
