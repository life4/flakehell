# Parsers

FlakeHell lints not only `*.py` files but also a number of additional formats:

+ [Markdown](https://en.wikipedia.org/wiki/Markdown) (`*.md`).
+ [ReStructuredText](https://en.wikipedia.org/wiki/ReStructuredText) (`*.rst`).
+ [Jupyter Notebook](https://jupyter.org/) (`*.ipynb`).
+ [pytest-mypy-plugins](https://github.com/typeddjango/pytest-mypy-plugins) tests (`*.yml`, `*.yaml`).

For `md` and `rst` code block must have explicitly specified language, either [python](https://pygments.org/docs/lexers/#pygments.lexers.python.PythonLexer) or [pycon](https://pygments.org/docs/lexers/#pygments.lexers.python.PythonConsoleLexer).

## Ignored codes

Parsers for `md`, `rst` and `yaml` ignore the following codes:

+ `E302` (`pycodestyle`): "expected %s blank lines, found %d"
+ `E303` (`pycodestyle`): "too many blank lines (%d)"
+ `E305` (`pycodestyle`): "expected %s blank lines after class or function definition, found %d"
+ `E402` (`pycodestyle`): "module level import not at top of file"

The reason is that all code blocks are validated in-place, with commenting out everything else. So, after that code blocks can be closer or further than pycodestyle expects.

## Performance

If you have performance issues because FlakeHell parses more files than needed, tune [ignore](https://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-ignore) to exclude specific files or directories, or [filename](https://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-filename) to exclude extensions.

However, keep in mind that FlakeHell has a few hacks to be as fast as possible:

1. It caches results. Cache invalidates after 24 hours or if the configuration was changed.
1. It doesn't run plugins against files without code blocks. Or against empty `*.py` files.
1. It doesn't create temporary files, all the magic is done on the fly.

So, most of the runs will be fast without any tuning.
