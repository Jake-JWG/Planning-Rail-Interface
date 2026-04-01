from datetime import datetime

from sqlalchemy.orm import Session

from app.models.entities import ReviewAction


def upsert_review(db: Session, match_id: int, status: str, reviewer_notes: str | None):
    review = db.query(ReviewAction).filter(ReviewAction.match_id == match_id).first()
    if review:
        review.status = status
        review.reviewer_notes = reviewer_notes
        review.reviewed_at = datetime.utcnow()
    else:
        review = ReviewAction(
            match_id=match_id,
            status=status,
            reviewer_notes=reviewer_notes,
            reviewed_at=datetime.utcnow(),
        )
        db.add(review)
    db.commit()
    return review
