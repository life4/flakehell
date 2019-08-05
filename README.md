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


![output example](./assets/grouped.png)

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

![plugins command output](./assets/plugins.png)

Show codes and messages for a specific plugin:

```bash
flakehell codes pyflakes
```

![codes command output](./assets/codes.png)

Run flake8 against the code:

```bash
flakehell lint
```

This command accepts all the same arguments as Flake8.

## Formatters

Formatters make errors output nice. Available formatters:

+ `colored` -- for humans.
+ `grouped` -- also colored, but all messages are explicitly grouped by file.
+ `json` -- no colors, only one json-dict per line for every error.

Also, you can specify `show_source = true` in the config to show line of source code where error occurred with syntax highlighting.

Colored:

![colored](./assets/colored.png)

Colored with source code:

![colored](./assets/colored-source.png)

Grouped:

![grouped](./assets/grouped.png)

Grouped with source code:

![grouped](./assets/grouped-source.png)

JSON:

![json](./assets/json.png)
