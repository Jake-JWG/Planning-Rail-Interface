import csv
import json
from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import AlertRun, SpatialMatch


def generate_alert(db: Session, run_type: str = "daily"):
    now = datetime.utcnow()
    window = timedelta(days=1) if run_type == "daily" else timedelta(days=7)
    since = now - window

    matches = db.execute(select(SpatialMatch).where(SpatialMatch.created_at >= since)).scalars().all()

    output_dir = Path("sample_data")
    output_dir.mkdir(exist_ok=True)
    json_path = output_dir / f"alerts_{run_type}.json"
    csv_path = output_dir / f"alerts_{run_type}.csv"

    payload = [
        {
            "id": m.id,
            "application_id": m.application_id,
            "railway_feature_id": m.railway_feature_id,
            "match_type": m.match_type,
            "confidence": m.confidence,
            "distance_meters": m.distance_meters,
            "evidence_text": m.evidence_text,
        }
        for m in matches
    ]

    json_path.write_text(json.dumps(payload, indent=2))
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(payload[0].keys()) if payload else ["id"])
        writer.writeheader()
        for row in payload:
            writer.writerow(row)

    db.add(AlertRun(run_type=run_type, run_timestamp=now, matches_included=len(matches)))
    db.commit()

    return {"run_type": run_type, "count": len(matches), "json": str(json_path), "csv": str(csv_path)}
