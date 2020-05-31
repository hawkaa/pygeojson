from .types import *
import json
from . import parsers


def load(f: IO[AnyStr]) -> GeoJSON:
    o = json.load(f)
    return parsers.geojson(o)
