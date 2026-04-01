from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.entities import PlanningApplication, SpatialMatch
from app.schemas.api import ConfigOut, IngestResponse, PlanningApplicationOut, ReviewPatch, SpatialMatchOut, TriggerResponse
from app.services.alerts import generate_alert
from app.services.ingestion import ingest_planning, ingest_rail
from app.services.matching import run_matching
from app.services.review import upsert_review

router = APIRouter()


@router.get("/applications", response_model=list[PlanningApplicationOut])
def list_applications(db: Session = Depends(get_db)):
    return db.query(PlanningApplication).all()


@router.get("/applications/{app_id}", response_model=PlanningApplicationOut)
def get_application(app_id: int, db: Session = Depends(get_db)):
    app = db.query(PlanningApplication).filter(PlanningApplication.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app


@router.get("/matches", response_model=list[SpatialMatchOut])
def list_matches(confidence: str | None = None, db: Session = Depends(get_db)):
    q = db.query(SpatialMatch)
    if confidence:
        q = q.filter(SpatialMatch.confidence == confidence)
    return q.all()


@router.get("/matches/{match_id}", response_model=SpatialMatchOut)
def get_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(SpatialMatch).filter(SpatialMatch.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.post("/ingest/planning", response_model=IngestResponse)
def run_planning_ingestion(db: Session = Depends(get_db)):
    return ingest_planning(db)


@router.post("/ingest/rail", response_model=IngestResponse)
def run_rail_ingestion(db: Session = Depends(get_db)):
    return ingest_rail(db)


@router.post("/run-matching", response_model=TriggerResponse)
def trigger_matching(db: Session = Depends(get_db)):
    result = run_matching(db)
    return TriggerResponse(message="Matching run complete", metadata=result)


@router.patch("/matches/{match_id}/review", response_model=TriggerResponse)
def patch_review(match_id: int, payload: ReviewPatch, db: Session = Depends(get_db)):
    review = upsert_review(db, match_id, payload.status, payload.reviewer_notes)
    return TriggerResponse(message="Review updated", metadata={"review_id": review.id, "status": review.status})


@router.post("/alerts/{run_type}", response_model=TriggerResponse)
def run_alert(run_type: str, db: Session = Depends(get_db)):
    if run_type not in {"daily", "weekly"}:
        raise HTTPException(status_code=400, detail="run_type must be daily or weekly")
    result = generate_alert(db, run_type)
    return TriggerResponse(message="Alert generated", metadata=result)


@router.get("/config", response_model=ConfigOut)
def get_config():
    return ConfigOut(
        default_threshold_meters=settings.default_threshold_meters,
        default_buffer_meters=settings.default_buffer_meters,
        planning_sources=settings.planning_sources,
        rail_sources=settings.rail_sources,
    )
