from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.entities import PlanningApplication, RailwayFeature, SpatialMatch
from app.utils.geospatial import load_geometry, to_bng


def _build_evidence(rule: str, distance: float | None, app_geom_type: str, rail_geom_type: str, threshold: float) -> str:
    return (
        f"rule={rule}; distance_m={None if distance is None else round(distance,2)}; "
        f"application_geom={app_geom_type}; rail_geom={rail_geom_type}; threshold={threshold}"
    )


def run_matching(db: Session, threshold_meters: float | None = None, screening_mode: bool = True):
    threshold = threshold_meters or settings.default_threshold_meters
    buffer_size = settings.default_buffer_meters

    db.execute(delete(SpatialMatch))

    apps = db.execute(select(PlanningApplication)).scalars().all()
    rails = db.execute(select(RailwayFeature)).scalars().all()
    created = 0

    for app in apps:
        app_geom = load_geometry(app.geometry_wkt)
        app_centroid = load_geometry(app.centroid_wkt)
        app_geom_bng = to_bng(app_geom)
        app_centroid_bng = to_bng(app_centroid)

        for rail in rails:
            rail_geom = load_geometry(rail.geometry_wkt)
            rail_geom_bng = to_bng(rail_geom)
            compare_geom = rail_geom_bng.buffer(buffer_size) if screening_mode and rail.feature_type.lower() == "line" else rail_geom_bng

            match_type = None
            confidence = None
            distance = app_geom_bng.distance(rail_geom_bng)

            if app_geom_bng.intersects(compare_geom):
                match_type = "intersects"
                confidence = "HIGH"
                distance = 0.0
            elif app_geom_bng.touches(compare_geom):
                match_type = "touches"
                confidence = "HIGH"
                distance = 0.0
            elif app_centroid_bng.distance(rail_geom_bng) <= threshold:
                match_type = "within_distance"
                confidence = "LOW" if app.geometry_source == "geocoded" else "MEDIUM"
                distance = app_centroid_bng.distance(rail_geom_bng)

            if match_type:
                evidence = _build_evidence(match_type, distance, app_geom.geom_type, rail_geom.geom_type, threshold)
                db.add(
                    SpatialMatch(
                        application_id=app.id,
                        railway_feature_id=rail.id,
                        match_type=match_type,
                        confidence=confidence,
                        distance_meters=distance,
                        threshold_meters=threshold,
                        evidence_text=evidence,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow(),
                    )
                )
                created += 1

    db.commit()
    return {"matches_created": created, "threshold_meters": threshold, "screening_mode": screening_mode}
