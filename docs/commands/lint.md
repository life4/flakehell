# **lint**: run flake8

Run patched flake8 against the code.

```bash
flakehell lint
```

This command accepts all the same arguments as Flake8.

Run linter against a file:

```bash
flakehell lint example.py
```

Run linter against a few dirs:

```bash
flakehell lint ./flakehell/ ./tests/
```

Show available arguments:

```bash
flakehell lint --help
```

Read [flake8 documentation](http://flake8.pycqa.org/en/latest/user/options.html) for list of available options.
