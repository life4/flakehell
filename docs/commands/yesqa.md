# **yesqa**: remove unused noqa

`# noqa` comment is a way [to disable flake8 check for line](http://flake8.pycqa.org/en/3.1.1/user/ignoring-errors.html). The problem is that these comments can be too general (and you'll miss another error on the same line) or not actual (and they will provide only visual noise without actually silencing anything).

The command is inspired by [yesqa](https://github.com/asottile/yesqa) tool and does the following:

+ Removes unused codes from `noQA`.
+ Removes bare `noQA` that says "ignore everything on this line" and is a bad practice.

Of course, it is fully integrated with FlakeHell and will take into account all rules from the config.

```python
# before
err=1  # noqa: E225, E117

# after
err=1  # noqa: E225
```

Usage is simple: just provide paths you want to fix:

```bash
flakehell yesqa ./example.py ./flakehell/
```
