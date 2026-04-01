"""Simple worker entrypoint for scheduled runs."""
from app.core.database import SessionLocal
from app.services.alerts import generate_alert


def run_daily_alert():
    db = SessionLocal()
    try:
        return generate_alert(db, "daily")
    finally:
        db.close()


if __name__ == "__main__":
    print(run_daily_alert())
