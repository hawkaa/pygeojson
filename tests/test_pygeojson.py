import pytest
from pygeojson import (
    Point,
    LineString,
    load,
    loads,
    dump,
    dumps,
    GeoJSONDecodeError,
    Feature,
    Polygon,
    FeatureCollection,
    GeometryCollection,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
)
from json import JSONDecodeError


@pytest.fixture
def load_json():
    def _load_json(path: str):
        with open("assets/%s" % (path,)) as f:
            return load(f)

    return _load_json


def test_feature_with_extra_attributes(load_json):
    o: Feature = load_json("feature_with_extra_attributes.json")
    assert o == Feature(
        id=None,
        bbox=None,
        type="Feature",
        geometry=None,
        properties={},
        extra_attributes={"foo": "bar"},
    )


def test_feature_with_id(load_json):
    o: Feature = load_json("feature_with_id.json")
    assert o == Feature(
        id="i_have_a_string_id",
        bbox=None,
        type="Feature",
        geometry=Point(coordinates=(102.0, 0.5)),
        properties={},
    )


def test_feature_with_null_geom(load_json):
    o: Feature = load_json("feature_with_null_geom.json")
    assert o == Feature(
        id=None, bbox=None, type="Feature", geometry=None, properties={},
    )


def test_feature_with_props(load_json):
    o: Feature = load_json("feature_with_props.json")
    assert o == Feature(
        id=1337,
        type="Feature",
        bbox=(100.0, 0.0, 101.0, 1.0),
        geometry=Polygon(
            coordinates=[
                [(100.0, 0.0), (101.0, 0.0), (101.0, 1.0), (100.0, 1.0), (100.0, 0.0)]
            ],
        ),
        properties={"prop0": "value0", "prop1": {"this": "that"}},
    )


def test_feature_without_geom(load_json):
    o: Feature = load_json("feature_without_geom.json")
    assert o == Feature(
        id=None, bbox=None, type="Feature", geometry=None, properties={},
    )


def test_feature(load_json):
    o: Feature = load_json("feature.json")
    assert o == Feature(
        id=None,
        type="Feature",
        bbox=None,
        geometry=LineString(
            coordinates=[(102.0, 0.0), (103.0, 1.0), (104.0, 0.0), (105.0, 1.0)]
        ),
        properties={},
    )


def test_equality(load_json):
    assert load_json("feature.json") == load_json("feature.json")


def test_inequality(load_json):
    assert load_json("feature.json") != load_json("feature_with_id.json")


def test_featurecollection_with_extra_attributes_access(load_json):
    o: FeatureCollection = load_json("featurecollection_with_extra_attributes.json")
    assert o["crs"]["properties"]["name"] == "urn:ogc:def:crs:EPSG::25832"


def test_featurecollection_not_equal(load_json):
    assert load_json("featurecollection.json") != load_json(
        "featurecollection_with_extra_attributes.json"
    )


def test_featurecollection(load_json):
    o: FeatureCollection = load_json("featurecollection.json")
    assert o == FeatureCollection(
        type="FeatureCollection",
        bbox=None,
        features=[
            Feature(
                id="i_have_a_string_id",
                geometry=Point(coordinates=(102.0, 0.5)),
                properties={"prop0": "value0"},
            ),
            Feature(
                id=1337,
                geometry=LineString(
                    coordinates=[(102.0, 0.0), (103.0, 1.0), (104.0, 0.0), (105.0, 1.0)]
                ),
                properties={"prop0": "value0", "prop1": 0.0},
            ),
        ],
    )


def test_geometrycollection(load_json):
    o: GeometryCollection = load_json("geometrycollection.json")
    assert o == GeometryCollection(
        type="GeometryCollection",
        geometries=[Point((100.0, 0.0)), LineString([(101.0, 0.0), (102.0, 1.0)])],
    )


def test_linestring(load_json):
    o: LineString = load_json("linestring.json")
    assert o == LineString(
        type="LineString",
        coordinates=[(102.0, 0.0), (103.0, 1.0), (104.0, 0.0), (105.0, 1.0)],
    )


def test_multilinestring(load_json):
    o: MultiLineString = load_json("multilinestring.json")
    assert o == MultiLineString(
        type="MultiLineString",
        coordinates=[[(100.0, 0.0), (101.0, 1.0)], [(102.0, 2.0), (103.0, 3.0)]],
    )


def test_multipoint(load_json):
    o: MultiPoint = load_json("multipoint.json")
    assert o == MultiPoint(type="MultiPoint", coordinates=[(100.0, 0.0), (101.0, 1.0)])


def test_multipolygon(load_json):
    o: MultiPolygon = load_json("multipolygon.json")
    assert o == MultiPolygon(
        type="MultiPolygon",
        coordinates=[
            [[(102.0, 2.0), (103.0, 2.0), (103.0, 3.0), (102.0, 3.0), (102.0, 2.0)]],
            [
                [(100.0, 0.0), (101.0, 0.0), (101.0, 1.0), (100.0, 1.0), (100.0, 0.0)],
                [(100.2, 0.2), (100.8, 0.2), (100.8, 0.8), (100.2, 0.8), (100.2, 0.2)],
            ],
        ],
    )


def test_not_a_geojson(load_json):
    with pytest.raises(GeoJSONDecodeError):
        load_json("not_a_geojson.json")


def test_not_a_json(load_json):
    with pytest.raises(JSONDecodeError):
        load_json("not_a_json.json")


def test_point(load_json):
    o: Point = load_json("point.json")
    assert o == Point(type="Point", coordinates=(102.0, 0.5))


def test_polygon(load_json):
    o: Polygon = load_json("polygon.json")
    assert o == Polygon(
        type="Polygon",
        coordinates=[
            [(100.0, 0.0), (101.0, 0.0), (101.0, 1.0), (100.0, 1.0), (100.0, 0.0)]
        ],
    )


def test_loads():
    assert (
        loads(
            """
    {
        "type": "Point",
        "coordinates": [1.0, 2.0]
    }"""
        )
        == Point((1.0, 2.0))
    )


def test_dumps():
    assert (
        dumps(Point((1.0, 2.0))) == """{"type": "Point", "coordinates": [1.0, 2.0]}"""
    )


@pytest.mark.parametrize(
    "file",
    [
        "feature_with_extra_attributes.json",
        "feature_with_id.json",
        "feature_with_null_geom.json",
        "feature_with_props.json",
        "feature_without_geom.json",
        "feature.json",
        "featurecollection_with_extra_attributes.json",
        "geometrycollection.json",
        "linestring.json",
        "multilinestring.json",
        "multipoint.json",
        "multipolygon.json",
        "point.json",
        "polygon.json",
    ],
)
def test_read_write_read(load_json, file):
    # If we read, dump, and read again, we should have the same results as read
    assert loads(dumps(load_json(file))) == load_json(file)


def test_dump(tmp_path):
    p = Point((1.0, 2.0))
    with open(tmp_path / "point.json", "w") as f:
        dump(p, f)
    with open(tmp_path / "point.json") as f:
        assert load(f) == p
