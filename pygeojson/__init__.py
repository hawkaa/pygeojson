from .types import *
import json
from . import parsers

__version__ = "0.1.1"


def load(f: IO[AnyStr]) -> GeoJSON:
    o = json.load(f)
    return parsers.geojson(o)
