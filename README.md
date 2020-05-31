# pygeojson 🗺

GeoJSON library for Python with [types](https://docs.python.org/3/library/typing.html).

The world doesn't need another
[GeoJSON library for python](https://github.com/jazzband/geojson), but it needs
a better one. The goal of this library is to provide a simple and typed data
model for GeoJSON such that y'all can get static code check and editor support
with [mypy](http://mypy-lang.org/). And of course, data should be data, so the
data model is not polluted with inheritance, custom methods, utilities,
extension or other "conveniences". Lastly, your data will be immutable!

`pygeojson` is built on top of
[`dataclasses`](https://docs.python.org/3/library/dataclasses.html) to provide
types, immutability and default value support. Models does not inherit from one
but instead we use
[`Union` types](https://docs.python.org/3/library/typing.html#typing.Union)
where applicable.

In addition, `pygeojson` comes with serialization and deserialization support
via the `dump`, `dumps`, `load` and `loads` functions.

## Installation

`pygeojson` requires Python 3.7 and up. Install it via `pipenv`:

```sh
pipenv install pygeojson
```

or `pip`:

```sh
pip install pygeojson
```

## Usage

TBD

## Data model

TBA
