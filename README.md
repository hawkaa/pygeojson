# pygeojson 🗺

GeoJSON library for Python with [types](https://docs.python.org/3/library/typing.html).

The world doesn't need another
[GeoJSON library for python](https://github.com/jazzband/geojson), but it needs
a better one. The goal of this library is to provide a simple and typed data
model for GeoJSON such that y'all can get static code check and editor support
with [mypy](http://mypy-lang.org/). And of course, data should be data, so the
data model is not polluted with inheritance, custom methods, utilities,
extension or other "conveniences". The data is of course immutable.

We have built `pygeojson` on top of Python's
[`dataclasses`](https://docs.python.org/3/library/dataclasses.html) to provide
type support and immutability. We do not use inheritance, but rather combine
the classes with [`Union` types](https://docs.python.org/3/library/typing.html#typing.Union)
where applicable.

In addition to the data representation, we provide serializers and deserializers
via the `dump`, `dumps`, `load`, `loads`, `load_feature_collection` and
`loads_feature_collection` functions.

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

### Data model

The classes provided in `pygeojson` matches the [GeoJSON specification
(RFC 7946)](https://tools.ietf.org/html/rfc7946) with some minor adjustments:

* Coordinates are tuples, not lists, e.g `(1.0, 2.0)`, not `[1.0, 2.0]`
* Attributes that are part of the GeoJSON standard are accessed as class
  members, e.g `point.coordinates` and not `point["coordinates"].
* Extra attributes not mentioned in the standard are set it the
  `extra_attributes` dictionary and accessed like a dictionary entry, e.g
  `point["custom_attribute"]`.

We provide the following classes that is a part of the `GeometryObject` union
type:

* `Point`
* `MultiPoint`
* `LineString`
* `MultiLineString`
* `Polygon`
* `MultiPolygon`
* `GeometryCollection`

In addition, the `GeoJSON` union type, in addition to the elements in
`GeometryObject` includes:

* `Feature`
* `FeatureCollection`

## Reading data

To read a file, use the `load` method:

```python
from pygeojson import load

with open("myfile.geojson") as f:
    my_object = load(f) # my_object is type GeoJSON

print(my_object.type) # prints the type of the object
if isinstance(my_object, Feature):
    print(my_object.geometry) # Prints a representation of the Feature's geometry

if isinstance(my_object, FeatureCollection):
    print(len(my_object.features)) # Prints the number of features in a feature collection
    print(my_object["name"]) # Prints an attribute from the original file that is not part of the geojson standard
```

Because most files are stored as `FeatureCollection`s, we provide a utility
function for returning that data type directly, and raising a `TypeError` if
it's not really a `FeatureCollection`:

```python
from pygeojson import load_feature_collection

with open("myfile.geojson") as f:
    my_feature_collection = load_feature_collection(f) # my_feature_collection is type FeatureCollection

```

Both `load` and `load_feature_collection` comes with a companion `loads`  and
`loads_feature_collection` for reading strings instead of files.


## Writing data

To write data, use the `dump` method:

```python
from pygeojson import FeatureCollection, Feature, Point

feature_collection = FeatureCollection(
  [
    Feature(
      Point((1.0, 2.0))
    )
  ],
   extra_attributes={"name": "foo"}
)
with open("feature_collection.geojson", "w") as f:
    dump(feature_collection, f)
```

You may also use `dumps` to serialize into a string instead of a file.

## Manipulating data

Since the data is immutable, one must always store modifications into a new
object. For instance, the following won't work:

```python
from pygeojson import Point

p = Point((1.0, 2.0), bbox=(0.0, 1.1, 2.2, 3.3))
p.coordinates = (2.0, 1.0)
"""
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<string>", line 4, in __setattr__
dataclasses.FrozenInstanceError: cannot assign to field 'coordinates'
"""
```

Instead, we use the `replace` method in `dataclasses`: 

```python
from pygeojson import Point
from dataclasses import replace
p = Point((1.0, 2.0), bbox=(0.0, 1.1, 2.2, 3.3))
p2 = replace(p, coordinates=(1.0, 2.0))
print(p2) # Prints "Point(coordinates=(1.0, 2.0), bbox=(0.0, 1.1, 2.2, 3.3), type='Point')"
```

We know it can take a little time getting used to, but we believe immutable data
structures is paramount in developing functions without side effects, which in
turn creates better and easier-to-maintain software.

# I want to contribute to this library

Please see [CONTRIBUTING.md](CONTRIBUTING.md).