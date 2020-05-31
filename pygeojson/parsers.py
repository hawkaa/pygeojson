from typing import List
from .types import (
    Point,
    LineString,
    Coordinates,
    GeoJSONDecodeError,
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


def coordinates1(o) -> Coordinates:
    if len(o) == 3:
        return (o[0], o[1], o[2])
    elif len(o) == 2:
        return (o[0], o[1])
    raise GeoJSONDecodeError("Coordinates must have 2 or 3 elements")


def coordinates2(o) -> List[Coordinates]:
    return [coordinates1(c) for c in o]


def coordinates3(o) -> List[List[Coordinates]]:
    return [coordinates2(c) for c in o]


def coordinates4(o) -> List[List[List[Coordinates]]]:
    return [coordinates3(c) for c in o]


def bbox(o) -> BoundingBox:
    return (o[0], o[1], o[2], o[3])


def point(o) -> Point:
    return Point(
        bbox=bbox(o["bbox"]) if "bbox" in o else None,
        coordinates=coordinates1(o["coordinates"]),
    )


def multipoint(o) -> MultiPoint:
    return MultiPoint(
        bbox=bbox(o["bbox"]) if "bbox" in o else None,
        coordinates=coordinates2(o["coordinates"]),
    )


def linestring(o) -> LineString:
    return LineString(
        bbox=bbox(o["bbox"]) if "bbox" in o else None,
        coordinates=coordinates2(o["coordinates"]),
    )


def multilinestring(o) -> MultiLineString:
    return MultiLineString(
        bbox=bbox(o["bbox"]) if "bbox" in o else None,
        coordinates=coordinates3(o["coordinates"]),
    )


def polygon(o) -> Polygon:
    return Polygon(
        bbox=bbox(o["bbox"]) if "bbox" in o else None,
        coordinates=coordinates3(o["coordinates"]),
    )


def multipolygon(o) -> MultiPolygon:
    return MultiPolygon(
        bbox=bbox(o["bbox"]) if "bbox" in o else None,
        coordinates=coordinates4(o["coordinates"]),
    )


def geometrycollection(o) -> GeometryCollection:
    return GeometryCollection(
        bbox=bbox(o["bbox"]) if "bbox" in o else None,
        geometries=[geometry(g) for g in o["geometries"]],
    )


def feature(o) -> Feature:
    return Feature(
        id=o.get("id", None),
        geometry=geometry(o["geometry"]) if o.get("geometry", None) else None,
        properties=o["properties"] if "properties" in o else {},
        bbox=bbox(o["bbox"]) if "bbox" in o else None,
        extra_attributes=dict(
            [
                (key, o[key])
                for key in o
                if key not in ["id", "geometry", "properties", "bbox", "type"]
            ]
        ),
    )


def featurecollection(o) -> FeatureCollection:
    return FeatureCollection(
        bbox=bbox(o["bbox"]) if "bbox" in o else None,
        features=[feature(f) for f in o["features"]],
        extra_attributes=dict(
            [(key, o[key]) for key in o if key not in ["bbox", "type", "features"]]
        ),
    )


def geometry(o) -> GeometryObject:
    type = o.get("type", None)
    if not type:
        raise GeoJSONDecodeError("No 'type' found in GeoJSON")
    if type == "Point":
        return point(o)
    if type == "MultiPoint":
        return multipoint(o)
    if type == "LineString":
        return linestring(o)
    if type == "MultiLineString":
        return multilinestring(o)
    if type == "Polygon":
        return polygon(o)
    if type == "GeometryCollection":
        return geometrycollection(o)
    if type == "MultiPolygon":
        return multipolygon(o)
    raise GeoJSONDecodeError("Unknown 'type' %s" % (type,))


def geojson(o) -> GeoJSON:
    type = o.get("type", None)
    if not type:
        raise GeoJSONDecodeError("No 'type' found in GeoJSON")
    if type in {
        "Point",
        "MultiPoint",
        "LineString",
        "MultiLineString",
        "Polygon",
        "MultiPolygon",
        "GeometryCollection",
    }:
        return geometry(o)
    if type == "Feature":
        return feature(o)
    if type == "FeatureCollection":
        return featurecollection(o)
    raise GeoJSONDecodeError("Unknown 'type' %s" % (type,))
