# FlakeHell

It's a [Flake8](https://gitlab.com/pycqa/flake8) wrapper to make it cool.

+ Sharable and remote configs.
+ Legacy-friendly: ability to get report only about new errors.
+ Use only specified plugins, not everything installed.
+ Manage codes per plugin.
+ Enable and disable plugins and codes by wildcard.
+ Make output beautiful.
+ [pyproject.toml](https://www.python.org/dev/peps/pep-0518/) support.
+ Show codes for installed plugins.
+ Show all messages and codes for a plugin.
+ Check that all required plugins are installed.
+ Syntax highlighting in messages and code snippets.
+ [PyLint](https://github.com/PyCQA/pylint) integration.

![output example](../assets/grouped.png)

```eval_rst
.. toctree::
    :maxdepth: 1
    :caption: Main Info

    config
    formatters
    plugins

.. toctree::
    :maxdepth: 1
    :caption: Commands

    lint
```
