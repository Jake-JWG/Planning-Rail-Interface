from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.routes import router
from app.core.database import Base, get_db
from app.services.ingestion import ingest_planning, ingest_rail
from app.services.matching import run_matching


def build_client():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    def _get_db():
        db = Session()
        try:
            yield db
        finally:
            db.close()

    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_db] = _get_db

    db = Session()
    ingest_planning(db)
    ingest_rail(db)
    run_matching(db)
    db.close()
    return TestClient(app)


def test_endpoints():
    client = build_client()
    assert client.get("/applications").status_code == 200
    matches = client.get("/matches")
    assert matches.status_code == 200
    if matches.json():
        mid = matches.json()[0]["id"]
        assert client.patch(f"/matches/{mid}/review", json={"status": "reviewed", "reviewer_notes": "ok"}).status_code == 200
