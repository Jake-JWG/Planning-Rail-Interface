from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.adapters.mock_planning import MockPlanningAdapter
from app.adapters.mock_rail import MockRailAdapter
from app.models.entities import (
    IngestionRun,
    PlanningApplication,
    PlanningApplicationVersion,
    RailwayDatasetVersion,
    RailwayFeature,
)
from app.utils.geospatial import compute_centroid_wkt, geocode_stub


def ingest_planning(db: Session):
    adapter = MockPlanningAdapter()
    records = adapter.fetch()
    created = 0
    updated = 0

    for rec in records:
        stmt = select(PlanningApplication).where(
            PlanningApplication.application_reference == rec["application_reference"],
            PlanningApplication.authority == rec["authority"],
        )
        existing = db.execute(stmt).scalar_one_or_none()

        geometry_wkt = rec.get("geometry_wkt")
        geometry_source = "source"
        if not geometry_wkt:
            point = geocode_stub(rec.get("address"), rec.get("postcode"))
            geometry_wkt = point.wkt
            geometry_source = "geocoded"

        centroid_wkt = compute_centroid_wkt(geometry_wkt)

        if existing:
            changed = existing.raw_payload != rec
            existing.description = rec.get("description")
            existing.status = rec.get("status")
            existing.last_updated = datetime.utcnow()
            existing.raw_payload = rec
            existing.geometry_wkt = geometry_wkt
            existing.centroid_wkt = centroid_wkt
            existing.geometry_source = geometry_source
            if changed:
                db.add(PlanningApplicationVersion(application_id=existing.id, raw_payload=rec))
            updated += 1
        else:
            app = PlanningApplication(
                application_reference=rec["application_reference"],
                authority=rec["authority"],
                description=rec.get("description"),
                address=rec.get("address"),
                postcode=rec.get("postcode"),
                status=rec.get("status"),
                application_type=rec.get("application_type"),
                source_url=rec.get("source_url"),
                geometry_wkt=geometry_wkt,
                centroid_wkt=centroid_wkt,
                geometry_source=geometry_source,
                raw_payload=rec,
                last_updated=datetime.utcnow(),
            )
            db.add(app)
            db.flush()
            db.add(PlanningApplicationVersion(application_id=app.id, raw_payload=rec))
            created += 1

    run = IngestionRun(
        source=adapter.source_name,
        run_timestamp=datetime.utcnow(),
        records_processed=len(records),
        records_created=created,
        records_updated=updated,
    )
    db.add(run)
    db.commit()
    return {"source": adapter.source_name, "processed": len(records), "created": created, "updated": updated}


def ingest_rail(db: Session):
    adapter = MockRailAdapter()
    records = adapter.fetch()
    created = 0
    updated = 0
    for rec in records:
        stmt = select(RailwayFeature).where(
            RailwayFeature.dataset_name == rec["dataset_name"],
            RailwayFeature.version == rec["version"],
            RailwayFeature.geometry_wkt == rec["geometry_wkt"],
        )
        existing = db.execute(stmt).scalar_one_or_none()
        if existing:
            updated += 1
        else:
            db.add(RailwayFeature(**rec))
            created += 1

    db.add(RailwayDatasetVersion(dataset_name=adapter.source_name, version_date=datetime.utcnow()))
    db.add(
        IngestionRun(
            source=adapter.source_name,
            run_timestamp=datetime.utcnow(),
            records_processed=len(records),
            records_created=created,
            records_updated=updated,
        )
    )
    db.commit()
    return {"source": adapter.source_name, "processed": len(records), "created": created, "updated": updated}
