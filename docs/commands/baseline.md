# **baseline**: integrate into a huge project

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

## Running flakehell against diff

Flake8 has `--diff` option to run checks only against specified diff. FlakeHell also supports it but additionally allows you to mix it with explicitly specified paths. For example:

```bash
git diff | flakehell lint --diff my_project/
```

Example of running [flake8-annotations](https://github.com/sco1/flake8-annotations) on [GitLab CI](https://docs.gitlab.com/ee/ci/) only against changed code in `my_project/`:

```yaml
flake8-annotations:
  image: "python:3.7-buster"
  stage: test
  rules:
    - if: $CI_MERGE_REQUEST_TARGET_BRANCH_SHA
      changes:
        - "my_project/**/*.py"
  script:
    - pip install flakehell flake8-annotations
    - git diff $CI_MERGE_REQUEST_TARGET_BRANCH_SHA | flakehell lint --diff my_project/
```

This option also can be mixed with baseline.
