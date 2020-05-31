import ast
from pathlib import Path
from flakehell.parsers import JupyterParser


GIVEN = r"""
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["Example notebook"]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import not_a_package\n",
    "{\"1\": 1}"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "One more line of text"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": { },
   "outputs": [],
   "source": [
    "{\"2\": 1}\n",
    "{\"2\": 2}"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
"""


EXPECTED = """
# In [1]:
import not_a_package
{"1": 1}

# In [2]:
{"2": 1}
{"2": 2}
"""


def test_markdown_parser(tmp_path: Path):
    path = tmp_path / 'example.md'
    path.write_text(GIVEN)
    actual = JupyterParser.parse(path=path)
    assert ''.join(actual) == EXPECTED

    # test that the result is a valid python code
    ast.parse(''.join(actual))
