# Railway Planning Proximity Monitor (MVP)

Production-oriented MVP for ingesting planning applications and railway assets, running spatial proximity/intersection matching, supporting review actions, and producing alert outputs.

## Features
- Modular ingestion adapters (planning + rail)
- Idempotent planning ingestion with version history
- Spatial matching engine (intersects, touches, within-distance)
- Confidence scoring (HIGH / MEDIUM / LOW)
- API endpoints for ingestion, matching, review, alerts, config
- Lightweight server-rendered UI for match list and details
- Docker Compose stack with PostGIS
- Tests for ingestion, geometry handling, matching, API

## Quick start
```bash
cp .env.example .env
docker compose -f docker/docker-compose.yml up --build
```

API docs: `http://localhost:8000/docs`
UI: `http://localhost:8000/`


## Vercel deployment
This repository is configured for zero-manual Vercel Python deployment:
- Entry point: `api/index.py` (exports FastAPI `app` and loads code from `src/app`).
- Build/runtime config: minimal `vercel.json` using only schema + `rewrites` (no legacy `builds` key).
- Runtime dependencies are pinned in `requirements.txt` for Vercel installs (no manual setup.py edits needed).
- Source code uses a `src/` layout (`src/app`) and `pyproject.toml` explicitly packages only `app`, preventing flat-layout multi-package discovery errors.
- `pyproject.toml` now explicitly limits package discovery to `src/app` and excludes non-app folders (`api`, `docker`, `migrations`, `sample_data`, `tests`).
- `.vercelignore` excludes non-runtime folders from deployment upload (`docker/`, `migrations/`, `sample_data/`, `tests/`).

## Local run (without Docker)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload
```

## Typical workflow
1. `POST /ingest/planning`
2. `POST /ingest/rail`
3. `POST /run-matching`
4. `POST /alerts/daily`

## Sample data
- `sample_data/planning_applications.json`
- `sample_data/railway_features.json`
- `sample_data/sample_alert_output.json`

## Testing
```bash
pytest
```

## Replacing mock datasets
Swap `MockPlanningAdapter` and `MockRailAdapter` with real adapters implementing the `fetch()` contract in `app/adapters/base.py`.
