from datetime import date, datetime
from typing import Any

from pydantic import BaseModel


class PlanningApplicationOut(BaseModel):
    id: int
    application_reference: str
    authority: str
    description: str | None = None
    status: str | None = None
    received_date: date | None = None
    geometry_wkt: str | None = None
    centroid_wkt: str | None = None

    class Config:
        from_attributes = True


class SpatialMatchOut(BaseModel):
    id: int
    application_id: int
    railway_feature_id: int
    match_type: str
    confidence: str
    distance_meters: float | None = None
    threshold_meters: float | None = None
    evidence_text: str

    class Config:
        from_attributes = True


class IngestResponse(BaseModel):
    source: str
    processed: int
    created: int
    updated: int


class ReviewPatch(BaseModel):
    status: str
    reviewer_notes: str | None = None


class ConfigOut(BaseModel):
    default_threshold_meters: float
    default_buffer_meters: float
    planning_sources: str
    rail_sources: str


class TriggerResponse(BaseModel):
    message: str
    metadata: dict[str, Any]
    timestamp: datetime = datetime.utcnow()
