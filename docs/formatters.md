# Formatters

Formatters make errors output nice. Available formatters:

+ `colored` -- for humans.
+ `gitlab` -- Gitlab CI [Code Quality artifact](https://docs.gitlab.com/ee/user/project/merge_requests/code_quality.html).
+ `grouped` -- also colored, but all messages are explicitly grouped by file.
+ `json` -- no colors, only one json-dict per line for every error.
+ `stat` -- show errors count for every code, grouped by plugins.
+ `default` -- classic Flake8 formatter. Booooring.

Also, you can specify `show_source = true` in the config to show line of source code where error occurred with syntax highlighting.

## Colored

```toml
[tool.flakehell]
format = "colored"
```

![output of colored formatter](../assets/colored.png)

## Colored with source code

```toml
[tool.flakehell]
format = "colored"
show_source = true
```

![output of colored formatter with source code](../assets/colored-source.png)

## Grouped

```toml
[tool.flakehell]
format = "grouped"
```

![output of grouped formatter](../assets/grouped.png)

## Grouped with source code

```toml
[tool.flakehell]
format = "grouped"
show_source = true
```

![output of grouped formatter with source code](../assets/grouped-source.png)

## Stat

```toml
[tool.flakehell]
format = "stat"
```

![output of stat formatter](../assets/stat.png)

## JSON

```toml
[tool.flakehell]
format = "json"
```

![output of json formatter](../assets/json.png)

## Gitlab

Output [Code Quality](https://docs.gitlab.com/ee/user/project/merge_requests/code_quality.html) artifact compatible with Gitlab CI.

```toml
[tool.flakehell]
format = "gitlab"
```

An example of Gitlab CI job (`.gitlab-ci.yml`):

```yaml
flakehell:
  image: python:3.7
  script:
    - pip3 install flakehell
    - flakehell lint --format=gitlab --output-file flakehell.json
  artifacts:
    reports:
      codequality: flakehell.json
```
