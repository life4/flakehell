# FlakeHell

It's a [Flake8](https://gitlab.com/pycqa/flake8) wrapper to make it cool.

+ Use only specified plugins, not everything installed.
+ Manage codes per plugin.
+ Enable and disable plugins and codes by wildcard.
+ Make output beautiful.
+ Show codes for installed plugins.
+ Show all messages and codes for a plugin.
+ Check that all required plugins are installed.
+ Syntax highlighting in messages and code snippets.


## Installation

```
python3 -m pip install --user flakehell
```


## Usage

First of all, let's create `pyproject.toml` config:

```toml
[tool.flakehell]
exclude = ["example.py"]
format = "grouped"
max_line_length = 90
show_source = true

[tool.flakehell.plugins]
pyflakes = ["+*", "-F401"]
flake8-quotes = ["+*"]
```

+ You can specify any flake8 settings in `[tool.flakehell]`.
+ `[tool.flakehell.plugins]` contains list of plugins and rules for them.

Show plugins that aren't installed yet:

```bash
flakehell missed
```

Show installed plugins, used plugins, specified rules, codes prefixes:

```bash
flakehell plugins
```

Show codes and messages for a specific plugin:

```bash
flakehell codes pyflakes
```

Run flake8 against the code:

```bash
flakehell lint
```

This command accepts all the same arguments as Flake8.
