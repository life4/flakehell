# ![FlakeHell](./assets/logo.png)

[![PyPI version](https://badge.fury.io/py/flakehell.svg)](https://badge.fury.io/py/flakehell)
[![Build Status](https://travis-ci.org/life4/flakehell.svg?branch=master)](https://travis-ci.org/life4/flakehell)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://readthedocs.org/projects/flakehell/badge/?version=latest)](https://flakehell.readthedocs.io/)

It's a [Flake8](https://gitlab.com/pycqa/flake8) wrapper to make it cool.

+ Shareable and remote configs.
+ Legacy-friendly: ability to get report only about new errors.
+ Caching for much better performance.
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
+ Allow codes intersection for different plugins.

![output example](./assets/grouped.png)

## Installation

```bash
python3 -m pip install --user flakehell
```

## Usage

First of all, let's create `pyproject.toml` config:

```toml
[tool.flakehell]
# optionally inherit from remote config (or local if you want)
base = "https://raw.githubusercontent.com/life4/flakehell/master/pyproject.toml"
# specify any flake8 options. For example, exclude "example.py":
exclude = ["example.py"]
# make output nice
format = "grouped"
# 80 chars aren't enough in 21 century
max_line_length = 90
# show line of source code in output
show_source = true

# list of plugins and rules for them
[tool.flakehell.plugins]
# include everything in pyflakes except F401
pyflakes = ["+*", "-F401"]
# enable only codes from S100 to S199
flake8-bandit = ["-*", "+S1??"]
# enable everything that starts from `flake8-`
"flake8-*" = ["+*"]
# explicitly disable plugin
flake8-docstrings = ["-*"]
```

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

Read [flakehell.readthedocs.io](https://flakehell.readthedocs.io/) for more information.

![](./assets/flaky.png)

The FlakeHell mascot (Flaky) is created by [@diana_leit](https://www.instagram.com/diana_leit/) and licensed under the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license.
