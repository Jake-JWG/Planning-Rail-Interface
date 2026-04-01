from app.models.entities import PlanningApplication, RailwayFeature, SpatialMatch
from app.services.matching import run_matching


def test_matching_accuracy(db_session):
    app = PlanningApplication(
        application_reference="A",
        authority="X",
        geometry_wkt="POLYGON((-0.102 51.498,-0.097 51.498,-0.097 51.502,-0.102 51.502,-0.102 51.498))",
        centroid_wkt="POINT(-0.0995 51.5)",
        geometry_source="source",
        raw_payload={},
    )
    rail = RailwayFeature(
        dataset_name="d",
        feature_type="line",
        geometry_wkt="LINESTRING(-0.101 51.499,-0.098 51.501)",
        version="v1",
    )
    db_session.add_all([app, rail])
    db_session.commit()

    result = run_matching(db_session)
    assert result["matches_created"] >= 1
    match = db_session.query(SpatialMatch).first()
    assert match.confidence == "HIGH"
