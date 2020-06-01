import ast
from pathlib import Path
from flakehell.parsers import RSTParser


GIVEN = """
I think I saw you in my sleep, Python

.. sourcecode:: pycon

    >>> # I think I saw you in my dreams
    >>> You = were(stitching="up the seams")
    'You were stitching up the seams'

On every broken promise that your body couldn't keep

.. code:: python

  from returns.result import Result, Success
  def may_fail(user_id: int) -> Result[float, str]:
      print('look at me!')

I think I saw you in my sleep
"""


EXPECTED = """
# I think I saw you in my sleep, Python

# .. sourcecode:: pycon

# I think I saw you in my dreams
You = were(stitching="up the seams")
# 'You were stitching up the seams'

# On every broken promise that your body c

# .. code:: python

from returns.result import Result, Success
def may_fail(user_id: int) -> Result[float, str]:
    print('look at me!')

# I think I saw you in my sleep
"""


def test_markdown_parser(tmp_path: Path):
    path = tmp_path / 'example.md'
    path.write_text(GIVEN)
    actual = RSTParser.parse(path=path)
    assert ''.join(actual) == EXPECTED

    # test that the result is a valid python code
    ast.parse(''.join(actual))
