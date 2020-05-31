from typing import Any, List
from .types import (
    Point,
    LineString,
    Coordinates,
    GeoJSONEncodeError,
    GeoJSON,
    Feature,
    GeometryObject,
    BoundingBox,
    Polygon,
    FeatureCollection,
    GeometryCollection,
    MultiPoint,
    MultiLineString,
    MultiPolygon,
)


def boundingbox(o: BoundingBox) -> Any:
    return list(o)


def coordinates1(o: Coordinates) -> Any:
    return list(o)


def coordinates2(o: List[Coordinates]) -> Any:
    return [coordinates1(c) for c in o]


def coordinates3(o: List[List[Coordinates]]) -> Any:
    return [coordinates2(c) for c in o]


def coordinates4(o: List[List[List[Coordinates]]]) -> Any:
    return [coordinates3(c) for c in o]


def feature(o: Feature) -> Any:
    r: Any = {"type": o.type, **o.extra_attributes}
    if o.id:
        r["id"] = o.id
    if o.geometry:
        r["geometry"] = geometry(o.geometry)
    if o.properties is not {}:
        r["properties"] = o.properties
    if o.bbox:
        r["bbox"] = boundingbox(o.bbox)
    return r


def featurecollection(o: FeatureCollection) -> Any:
    r = {
        "type": o.type,
        "features": [feature(f) for f in o.features],
        **o.extra_attributes,
    }
    if o.bbox:
        r["bbox"] = boundingbox(o.bbox)
    return r


def geometry(o: GeometryObject) -> Any:
    if isinstance(o, Point):
        r = {"type": o.type, "coordinates": coordinates1(o.coordinates)}
        if o.bbox:
            r["bbox"] = boundingbox(o.bbox)
        return r
    if isinstance(o, MultiPoint) or isinstance(o, LineString):
        r = {"type": o.type, "coordinates": coordinates2(o.coordinates)}
        if o.bbox:
            r["bbox"] = boundingbox(o.bbox)
        return r
    if isinstance(o, MultiLineString) or isinstance(o, Polygon):
        r = {"type": o.type, "coordinates": coordinates3(o.coordinates)}
        if o.bbox:
            r["bbox"] = boundingbox(o.bbox)
        return r
    if isinstance(o, MultiPolygon):
        r = {"type": o.type, "coordinates": coordinates4(o.coordinates)}
        if o.bbox:
            r["bbox"] = boundingbox(o.bbox)
        return r
    if isinstance(o, GeometryCollection):
        r = {"type": o.type, "geometries": [geometry(g) for g in o.geometries]}
        if o.bbox:
            r["bbox"] = boundingbox(o.bbox)
        return r

    raise GeoJSONEncodeError("Unknown geometry object %s" % (o,))


def geojson(o: GeoJSON) -> Any:
    if (
        isinstance(o, Point)
        or isinstance(o, MultiPoint)
        or isinstance(o, LineString)
        or isinstance(o, MultiLineString)
        or isinstance(o, Polygon)
        or isinstance(o, MultiPolygon)
        or isinstance(o, GeometryCollection)
    ):
        return geometry(o)
    if isinstance(o, Feature):
        return feature(o)
    if isinstance(o, FeatureCollection):
        return featurecollection(o)

    raise GeoJSONEncodeError("Unknown GeoJSON object %s" % (o,))
