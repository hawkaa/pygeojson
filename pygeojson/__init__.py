from .types import *
import json
from . import deserializers
from . import serializers

__version__ = "0.2.0"


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


def loads_feature_collection(s: AnyStr) -> FeatureCollection:
    fc = loads(s)
    if isinstance(fc, FeatureCollection):
        return fc
    raise TypeError("Tried to load an object that was not a FeatureCollection")


def load_feature_collection(f: IO[str]) -> FeatureCollection:
    fc = load(f)
    if isinstance(fc, FeatureCollection):
        return fc
    raise TypeError("Tried to load an object that was not a FeatureCollection")
