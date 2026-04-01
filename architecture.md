# Architecture Overview

## Phase 1 - structure
```
/app
  /api
  /core
  /models
  /schemas
  /services
  /adapters
  /workers
  /utils
  /templates
/tests
/migrations
/docker
/sample_data
```

## Phase 2 - backend + ingestion + matching
- FastAPI app in `app/main.py`
- SQLAlchemy models in `app/models/entities.py`
- Ingestion services in `app/services/ingestion.py`
- Matching engine in `app/services/matching.py`

## Phase 3 - API + alerting
- REST endpoints in `app/api/routes.py`
- Alert generation in `app/services/alerts.py`

## Phase 4 - UI
- Server-rendered pages with Jinja2 + Leaflet

## Phase 5 - deployment + QA
- Docker/PostGIS in `docker/docker-compose.yml`
- SQL migration script in `migrations/001_init.sql`
- Pytest suite under `/tests`

## CRS strategy
- Geometries are ingested as WKT in EPSG:4326.
- Distance computations transform geometries to EPSG:27700 via PyProj/Shapely.

## Explainability
Every match stores deterministic evidence text including triggered rule, distance, geometry types, and threshold.
