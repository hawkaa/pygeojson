# Contrbuting

...

## Hacking

Set up the project with `poetry`:

```sh
poetry install
```

Run the tests:

```sh
poetry run python -m pytest
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
poetry run semantic-release version
```

Then, create the changelog and update the `CHANGELOG.md` manually:

```sh
poetry run semantic-release changelog
```

Also, update the version number in `pyproject.toml` to the one
created by `semantic-python`.

Amend the changelog changes and new version to the commit:

```sh
git add CHANGELOG.md pyproject.toml
git commit --amend
```

Publish to PyPi:

```sh
poetry build && poetry publish
```
