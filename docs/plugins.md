# Plugins

The main reason why flake8 is so popular is a powerful plugins' support. FlakeHell is fully compatible with all plugins. Let's talk about most important ones.

+ [pyflakes](https://github.com/PyCQA/pyflakes) -- checks only obvious bugs and never code style. There are no opinionated checks. Pyflakes must be enabled in any project, and all error must be fixed.
+ [pycodestyle](https://github.com/PyCQA/pycodestyle) -- most important code style checker. Controls compatibility with [PEP-8](https://www.python.org/dev/peps/pep-0008/) that is standard de-facto for how Python code should look like. Initially, with tool was called pep8, but [renamed after Guido's request](https://github.com/PyCQA/pycodestyle/issues/466).
+ [PyLint](https://github.com/PyCQA/pylint) -- alternative linter. Has many checks, some of them is opinionated and can be difficult to satisfy. However, most of the checks are really useful. FlakeHell has it's own integration for it.
+ Discover more plugins in [awesome-flake8-extensions](https://github.com/DmytroLitvinov/awesome-flake8-extensions) list.

Pyflakes and pycodestyle are default dependencies of Flake8. If you just install and run Flake8 in clean environment, you'll see their checks. FlakeHell preserve this behavior, and by default runs all checks from pyflakes and pycodestyle. In another word, default FlakeHell config looks like this:

```toml
[tool.flakehell.plugins]
pyflakes = ["+*"]
pycodestyle = ["+*"]
```

However, best practice is enable as many plugins and checks as you can. It helps you to have readable and reliable code and never [bikeshed](http://bikeshed.com/). Let machines help you.
