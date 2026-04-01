from shapely.geometry import Polygon

from app.utils.geospatial import load_geometry, to_bng


def test_geometry_validation_and_transform():
    malformed = "POLYGON((0 0,1 1,1 0,0 1,0 0))"
    geom = load_geometry(malformed)
    assert geom.is_valid
    bng = to_bng(Polygon([(0, 51), (0.1, 51), (0.1, 51.1), (0, 51.1)]))
    assert bng.area > 0
