from app.models.entities import PlanningApplication
from app.services.ingestion import ingest_planning


def test_ingestion_idempotency(db_session):
    first = ingest_planning(db_session)
    second = ingest_planning(db_session)
    assert first["created"] == 3
    assert second["created"] == 0
    assert db_session.query(PlanningApplication).count() == 3
