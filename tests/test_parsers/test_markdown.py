import ast
from pathlib import Path
from flakehell.parsers import MarkdownParser


GIVEN = """
# Example

This is example of markdown file

```python
a = 1
print('oh hi mark')
```

Emphasized:

```python hl_lines="1"
emphasized_imaginary_function()
```

PyCon:

```pycon
>>> print("Hello")
'Hello'
>>> banana = "banana"
>>> for character in banana:
...     print(characterr)

```

1. Indented:
    ```python
    if 'look at me!':
        print('i am indented!')
    ```
"""


EXPECTED = """
# # Example

# This is example of markdown file

# ```python
a = 1
print('oh hi mark')
# ```

# Emphasized:

# ```python hl_lines="1"
emphasized_imaginary_function()
# ```

# PyCon:

# ```pycon
print("Hello")
# 'Hello'
banana = "banana"
for character in banana:
    print(characterr)

# ```

# 1. Indented:
# ```python
if 'look at me!':
    print('i am indented!')
# ```
"""


def test_markdown_parser(tmp_path: Path):
    path = tmp_path / 'example.md'
    path.write_text(GIVEN)
    actual = MarkdownParser.parse(path=path)
    assert ''.join(actual) == EXPECTED

    # test that the result is a valid python code
    ast.parse(''.join(actual))
