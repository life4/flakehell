import ast
from pathlib import Path
from flakehell.parsers import YAMLParser


GIVEN = """
- case: context_ask1
  disable_cache: true
  main: |
    from returns.context import Context
    reveal_type(Context.ask())  # N: ...

- case: context_wrong_cast
  disable_cache: true
  main: |
    from returns.context import RequiresContext
    first: RequiresContext[ValueError, TypeError]  # we can only return type
    second: RequiresContext[Exception, Exception] = first
  out: |
    main:4: error: ...

- case: context_covariant_cast
  disable_cache: true
  main: |
    from returns.context import RequiresContext
    class A(object):
        a = 1
"""


EXPECTED = """
reveal_type = lambda x: x  # noqa
# disable_cache: true
# main: |
from returns.context import Context
reveal_type(Context.ask())  # N: ...

# - case: context_wrong_cast
# disable_cache: true
# main: |
from returns.context import RequiresContext
first: RequiresContext[ValueError, TypeError]  # we can only return type
second: RequiresContext[Exception, Exception] = first
# out: |
# main:4: error: ...

# - case: context_covariant_cast
# disable_cache: true
# main: |
from returns.context import RequiresContext
class A(object):
    a = 1
"""


def test_markdown_parser(tmp_path: Path):
    path = tmp_path / 'test_example.yml'
    path.write_text(GIVEN.lstrip())
    actual = YAMLParser.parse(path=path)
    assert ''.join(actual) == EXPECTED.lstrip()

    # test that the result is a valid python code
    ast.parse(''.join(actual))
