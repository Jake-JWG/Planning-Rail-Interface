from shapely import wkt
from shapely.geometry import Point
from shapely.ops import transform
from pyproj import Transformer

TO_BNG = Transformer.from_crs("EPSG:4326", "EPSG:27700", always_xy=True)


def load_geometry(wkt_value: str):
    geom = wkt.loads(wkt_value)
    if not geom.is_valid:
        geom = geom.buffer(0)
    return geom


def to_bng(geom):
    return transform(TO_BNG.transform, geom)


def compute_centroid_wkt(geom_wkt: str) -> str:
    geom = load_geometry(geom_wkt)
    return geom.centroid.wkt


def geocode_stub(address: str | None, postcode: str | None) -> Point:
    seed = f"{address or ''}{postcode or ''}"
    val = sum(ord(c) for c in seed) % 1000
    return Point(-0.1 + val / 50000, 51.5 + val / 50000)
