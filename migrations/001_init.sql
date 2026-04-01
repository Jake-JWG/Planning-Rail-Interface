-- PostgreSQL/PostGIS migration
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS planning_applications (
  id SERIAL PRIMARY KEY,
  application_reference VARCHAR(100) NOT NULL,
  authority VARCHAR(120) NOT NULL,
  description TEXT,
  address TEXT,
  postcode VARCHAR(20),
  status VARCHAR(50),
  application_type VARCHAR(50),
  received_date DATE,
  validated_date DATE,
  decision_date DATE,
  last_updated TIMESTAMP,
  source_url TEXT,
  geometry GEOMETRY,
  centroid GEOMETRY,
  raw_payload JSONB,
  UNIQUE(application_reference, authority)
);

CREATE INDEX IF NOT EXISTS idx_planning_geom_gist ON planning_applications USING GIST (geometry);
CREATE INDEX IF NOT EXISTS idx_planning_centroid_gist ON planning_applications USING GIST (centroid);
CREATE INDEX IF NOT EXISTS idx_planning_ref_authority ON planning_applications(application_reference, authority);
CREATE INDEX IF NOT EXISTS idx_planning_dates ON planning_applications(received_date, validated_date, decision_date);

CREATE TABLE IF NOT EXISTS planning_application_versions (
  id SERIAL PRIMARY KEY,
  application_id INTEGER NOT NULL REFERENCES planning_applications(id),
  version_timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
  raw_payload JSONB
);

CREATE TABLE IF NOT EXISTS railway_features (
  id SERIAL PRIMARY KEY,
  dataset_name VARCHAR(100) NOT NULL,
  feature_type VARCHAR(50) NOT NULL,
  geometry GEOMETRY NOT NULL,
  version VARCHAR(30) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_rail_geom_gist ON railway_features USING GIST (geometry);

CREATE TABLE IF NOT EXISTS railway_dataset_versions (
  id SERIAL PRIMARY KEY,
  dataset_name VARCHAR(100) NOT NULL,
  version_date TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS spatial_matches (
  id SERIAL PRIMARY KEY,
  application_id INTEGER NOT NULL REFERENCES planning_applications(id),
  railway_feature_id INTEGER NOT NULL REFERENCES railway_features(id),
  match_type VARCHAR(30) NOT NULL,
  confidence VARCHAR(10) NOT NULL,
  distance_meters DOUBLE PRECISION,
  threshold_meters DOUBLE PRECISION,
  evidence_text TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS review_actions (
  id SERIAL PRIMARY KEY,
  match_id INTEGER NOT NULL REFERENCES spatial_matches(id),
  status VARCHAR(30) NOT NULL,
  reviewer_notes TEXT,
  reviewed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alert_runs (
  id SERIAL PRIMARY KEY,
  run_type VARCHAR(20) NOT NULL,
  run_timestamp TIMESTAMP NOT NULL,
  matches_included INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS ingestion_runs (
  id SERIAL PRIMARY KEY,
  source VARCHAR(100) NOT NULL,
  run_timestamp TIMESTAMP NOT NULL,
  records_processed INTEGER NOT NULL,
  records_created INTEGER NOT NULL,
  records_updated INTEGER NOT NULL
);
