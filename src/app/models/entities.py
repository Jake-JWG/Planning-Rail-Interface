from datetime import datetime, date

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class PlanningApplication(Base):
    __tablename__ = "planning_applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_reference: Mapped[str] = mapped_column(String(100), nullable=False)
    authority: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    address: Mapped[str | None] = mapped_column(Text)
    postcode: Mapped[str | None] = mapped_column(String(20))
    status: Mapped[str | None] = mapped_column(String(50))
    application_type: Mapped[str | None] = mapped_column(String(50))
    received_date: Mapped[date | None] = mapped_column(Date)
    validated_date: Mapped[date | None] = mapped_column(Date)
    decision_date: Mapped[date | None] = mapped_column(Date)
    last_updated: Mapped[datetime | None] = mapped_column(DateTime)
    source_url: Mapped[str | None] = mapped_column(Text)
    geometry_wkt: Mapped[str | None] = mapped_column(Text)
    centroid_wkt: Mapped[str | None] = mapped_column(Text)
    geometry_source: Mapped[str] = mapped_column(String(20), default="source")
    raw_payload: Mapped[dict] = mapped_column(JSON, default={})

    versions: Mapped[list["PlanningApplicationVersion"]] = relationship(back_populates="application", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("application_reference", "authority", name="uq_app_ref_authority"),)


class PlanningApplicationVersion(Base):
    __tablename__ = "planning_application_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("planning_applications.id"), nullable=False)
    version_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    raw_payload: Mapped[dict] = mapped_column(JSON, default={})

    application: Mapped[PlanningApplication] = relationship(back_populates="versions")


class RailwayFeature(Base):
    __tablename__ = "railway_features"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dataset_name: Mapped[str] = mapped_column(String(100), nullable=False)
    feature_type: Mapped[str] = mapped_column(String(50), nullable=False)
    geometry_wkt: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[str] = mapped_column(String(30), nullable=False)


class RailwayDatasetVersion(Base):
    __tablename__ = "railway_dataset_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dataset_name: Mapped[str] = mapped_column(String(100), nullable=False)
    version_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SpatialMatch(Base):
    __tablename__ = "spatial_matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("planning_applications.id"), nullable=False)
    railway_feature_id: Mapped[int] = mapped_column(ForeignKey("railway_features.id"), nullable=False)
    match_type: Mapped[str] = mapped_column(String(30), nullable=False)
    confidence: Mapped[str] = mapped_column(String(10), nullable=False)
    distance_meters: Mapped[float | None] = mapped_column(Float)
    threshold_meters: Mapped[float | None] = mapped_column(Float)
    evidence_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ReviewAction(Base):
    __tablename__ = "review_actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("spatial_matches.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="pending")
    reviewer_notes: Mapped[str | None] = mapped_column(Text)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime)


class AlertRun(Base):
    __tablename__ = "alert_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_type: Mapped[str] = mapped_column(String(20), nullable=False)
    run_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    matches_included: Mapped[int] = mapped_column(Integer, default=0)


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    run_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    records_processed: Mapped[int] = mapped_column(Integer, default=0)
    records_created: Mapped[int] = mapped_column(Integer, default=0)
    records_updated: Mapped[int] = mapped_column(Integer, default=0)
