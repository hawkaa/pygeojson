# Contrbuting

...

## Hacking

Set up the project with `poetry`:

```sh
poetry install
```

Run the tests:

```sh
poetry run pytest
```

Run type/lint check:

```sh
poetry run mypy pygeojson
```

Check formatting:

```sh
poetry run black
```

## Publishing

This project uses
[conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) and 
[`python-semantic-release`](https://github.com/relekang/python-semantic-release)
to generate version numbers and changelogs.

First, check out a new branch and create a new version:
```sh
poetry run python-semantic-release-version
```
