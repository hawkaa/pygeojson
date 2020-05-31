from typing import Tuple, Union, Optional, List, Dict, Any, AnyStr, Type, IO
from dataclasses import dataclass, field

#
# Base Types
#
Number = Union[float, int]
BoundingBox = Tuple[Number, Number, Number, Number]
Coordinates = Union[Tuple[Number, Number], Tuple[Number, Number, Number]]
Position = Union[
    Coordinates,
    List[Coordinates],
    List[List[Coordinates]],
    List[List[List[Coordinates]]],
]


GeoJSON = Union[
    "Feature",
    "FeatureCollection",
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
    "GeometryCollection",
]

GeometryObject = Union[
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
    "GeometryCollection",
]


@dataclass(frozen=True)
class Feature:
    id: Optional[Union[Number, str]] = None
    geometry: Optional[GeometryObject] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    bbox: Optional[BoundingBox] = None
    type: str = "Feature"
    extra_attributes: Dict[str, Any] = field(default_factory=dict)

    def __getitem__(self, item):
        return self.extra_attributes[item]


@dataclass(frozen=True)
class FeatureCollection:
    features: List[Feature]
    bbox: Optional[BoundingBox] = None
    type: str = "FeatureCollection"
    extra_attributes: Dict[str, Any] = field(default_factory=dict)

    def __getitem__(self, item):
        return self.extra_attributes[item]


@dataclass(frozen=True)
class Point:
    coordinates: Coordinates
    bbox: Optional[BoundingBox] = None
    type: str = "Point"


@dataclass(frozen=True)
class MultiPoint:
    coordinates: List[Coordinates]
    bbox: Optional[BoundingBox] = None
    type: str = "MultiPoint"


@dataclass(frozen=True)
class LineString:
    coordinates: List[Coordinates]
    bbox: Optional[BoundingBox] = None
    type: str = "LineString"


@dataclass(frozen=True)
class MultiLineString:
    coordinates: List[List[Coordinates]]
    bbox: Optional[BoundingBox] = None
    type: str = "MultiLineString"


@dataclass(frozen=True)
class Polygon:
    coordinates: List[List[Coordinates]]
    bbox: Optional[BoundingBox] = None
    type: str = "Polygon"


@dataclass(frozen=True)
class MultiPolygon:
    coordinates: List[List[List[Coordinates]]]
    bbox: Optional[BoundingBox] = None
    type: str = "MultiPolygon"


@dataclass(frozen=True)
class GeometryCollection:
    geometries: List[GeometryObject]
    bbox: Optional[BoundingBox] = None
    type: str = "GeometryCollection"


class GeoJSONDecodeError(Exception):
    pass


class GeoJSONEncodeError(Exception):
    pass
