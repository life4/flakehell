# ![FlakeHell](./assets/logo.png)

[![PyPI version](https://badge.fury.io/py/flakehell.svg)](https://badge.fury.io/py/flakehell)
[![Build Status](https://cloud.drone.io/api/badges/life4/flakehell/status.svg)](https://cloud.drone.io/life4/flakehell)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://readthedocs.org/projects/flakehell/badge/?version=latest)](https://flakehell.readthedocs.io/)

It's a [Flake8](https://gitlab.com/pycqa/flake8) wrapper to make it cool.

+ [Lint md, rst, ipynb, and more](https://flakehell.readthedocs.io/parsers.html).
+ [Shareable and remote configs](https://flakehell.readthedocs.io/config.html#base).
+ [Legacy-friendly](https://flakehell.readthedocs.io/commands/baseline.html): ability to get report only about new errors.
+ Caching for much better performance.
+ [Use only specified plugins](https://flakehell.readthedocs.io/config.html#plugins), not everything installed.
+ [Make output beautiful](https://flakehell.readthedocs.io/formatters.html).
+ [pyproject.toml](https://www.python.org/dev/peps/pep-0518/) support.
+ [Check that all required plugins are installed](https://flakehell.readthedocs.io/commands/missed.html).
+ [Syntax highlighting in messages and code snippets](https://flakehell.readthedocs.io/formatters.html#colored-with-source-code).
+ [PyLint](https://github.com/PyCQA/pylint) integration.
+ [Remove unused noqa](https://flakehell.readthedocs.io/commands/yesqa.html).
+ [Powerful GitLab support](https://flakehell.readthedocs.io/formatters.html#gitlab).
+ Codes management:
    + Manage codes per plugin.
    + Enable and disable plugins and codes by wildcard.
    + [Show codes for installed plugins](https://flakehell.readthedocs.io/commands/plugins.html).
    + [Show all messages and codes for a plugin](https://flakehell.readthedocs.io/commands/codes.html).
    + Allow codes intersection for different plugins.

![output example](./assets/grouped.png)

## Compatibility

FlakeHell supports all flake8 plugins, formatters, and configs. However, FlakeHell has it's own beautiful way to configure enabled plugins and codes. So, options like `--ignore` and `--select` unsupported. You can have flake8 and FlakeHell in one project if you want but enabled plugins should be explicitly specified.

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

## Contributing

Contributions are welcome! A few ideas what you can contribute:

+ Improve documentation.
+ Add more tests.
+ Improve performance.
+ Found a bug? Fix it!
+ Made an article about FlakeHell? Great! Let's add it into the `README.md`.
+ Don't have time to code? No worries! Just tell your friends and subscribers about the project. More users -> more contributors -> more cool features.

A convenient way to run tests is using [DepHell](https://github.com/dephell/dephell):

```bash
curl -L dephell.org/install | python3
dephell venv create --env=pytest
dephell deps install --env=pytest
dephell venv run --env=pytest
```

Bug-tracker is disabled by-design to shift contributions from words to actions. Please, help us make the project better and don't stalk maintainers in social networks and on the street.

Thank you :heart:

![](./assets/flaky.png)

The FlakeHell mascot (Flaky) is created by [@illustrator.way](https://www.instagram.com/illustrator.way/) and licensed under the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license.
