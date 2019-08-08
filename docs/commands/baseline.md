# **baseline**: integrate into huge project

Baseline allows you to remember the current project state and then show only new errors, ignoring old ones.

First of all, let's create baseline.

```bash
flakehell baseline > baseline.txt
```

Then specify path to the baseline file:

```toml
[tool.flakehell]
baseline = "baseline.txt"
```

Now, `flakehell lint` command will ignore all your current errors. It will report only about new errors, all errors in a new code, or if old line of code was modified.
