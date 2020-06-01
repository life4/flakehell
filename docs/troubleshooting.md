# Troubleshooting

FlakeHell has flake8 deep in its core but they are different. So, when migrating from flake8 there are some details that can be unexpected from your previous experience. So, let's talk how to turn such details from your enemies to your best friends.

## Flake8 configurations are ignored

FlakeHell reads flake8 configs and supports most of the options. However, some options (like `ignore` and `select`) ignored by design. The motivation is to get rid of over-complicated and unstable way how flake8 select and deselect plugins and provide a better way to do so. See [ignored options](https://flakehell.readthedocs.io/config.html#ignored-options) for details.

## It is slow

First of all, let's talk why FlakeHell is fast:

1. It caches results. Cache invalidates after 24 hours or if the configuration was changed.
1. It doesn't run plugins against files without code blocks or against empty `*.py` files.
1. It doesn't create temporary files for linting non-python files, all the magic is done on the fly.
1. It runs only explicitly specified plugins. If a plugin is not specified in the config, it won't be run.

And now, why it can be slow:

1. We use the same plugins-discovery mechanic as flake8 does, and it is slow. It requires to scan all installed libraries on every run. As a solution, keep FlakeHell in a separate virtual environment. There are a few tools that can help with it: [dephell](https://dephell.readthedocs.io/cmd-jail-install.html), [pipsi](https://github.com/mitsuhiko/pipsi), [pipx](https://github.com/pipxproject/pipx).
1. FlakeHell lints not only `*.py` files but also `*.md`, `*.rst` and a few more. See [parsers](parsers) section for the details. If you don't need it, tune [ignore](https://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-ignore) to exclude specific files or directories, or [filename](https://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-filename) to exclude extensions.

## Some plugins are ignored

There are few requirements for a plugin to be run:

1. It must be installed in the same venv as FlakeHell.
1. It must be explicitly specified in `plugins` section in [config](config).

Use [missed](commands/missed) command to see selected but not installed plugins and [plugins](commands/plugins) command to see installed but not selected plugins.

By default, FlakeHell runs only [pyflakes](https://github.com/PyCQA/pyflakes) and [pycodestyle](https://github.com/PyCQA/pycodestyle). If you want just run every plugin in the environment (don't do this), there is a trick how to select everything:

```toml
[tool.flakehell.plugins]
"*" = ["+*"]
```

## My IDE fails

Flake8 plugin for IDE expects output to be in a specific format. However, FlakeHell uses different, human-friendly, output format. Add `--format=default` option to use default flake8 output format. Also, there is `--format=json` for, you know, [JSON output per-line](http://ndjson.org/).

## I don't want to have pyproject.toml

`pyproject.toml` is a new configuration format for Python tools. It was introduced in [PEP 518](https://www.python.org/dev/peps/pep-0518/) and is widely supported by many tools. And that's a good thing that helps to clean-up the project root for a lot of separate config for different tools. So, it's a new way-to-go for all the Python tooling, give it a try.

## It must be flake8 compatible

Every detail that is not flake8 compatible was added in FlakeHell only to make it better. However, if you, by some reason, still want to use FlakeHell and Flake8 in the same project, it is easy to have done. FlakeHell doesn't monkey patch anything in Flake8, so it will work as expected. The only thing you should make is to provide `tool.flakehell.plugins` section in `pyproject.toml`.
