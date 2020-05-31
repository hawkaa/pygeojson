from .types import *
import json
from . import deserializers
from . import serializers

__version__ = "0.1.1"


def loads(s: AnyStr) -> GeoJSON:
    return deserializers.geojson(json.loads(s))


def load(f: IO[str]) -> GeoJSON:
    return deserializers.geojson(json.load(f))


def dump(g: GeoJSON, fp: IO[str]) -> None:
    o = serializers.geojson(g)
    return json.dump(o, fp)


def dumps(g: GeoJSON) -> str:
    o = serializers.geojson(g)
    return json.dumps(o)
