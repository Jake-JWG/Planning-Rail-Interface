from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api.routes import router
from app.core.database import Base, engine, get_db
from app.models.entities import SpatialMatch, PlanningApplication, ReviewAction

app = FastAPI(title="Railway Planning Proximity Monitor")
app.include_router(router)
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse)
def ui_matches(request: Request, db: Session = Depends(get_db), confidence: str | None = None):
    q = db.query(SpatialMatch)
    if confidence:
        q = q.filter(SpatialMatch.confidence == confidence)
    matches = q.all()
    return templates.TemplateResponse("matches.html", {"request": request, "matches": matches})


@app.get("/ui/matches/{match_id}", response_class=HTMLResponse)
def ui_match_detail(request: Request, match_id: int, db: Session = Depends(get_db)):
    match = db.query(SpatialMatch).filter(SpatialMatch.id == match_id).first()
    if not match:
        return HTMLResponse("Not Found", status_code=404)
    app_row = db.query(PlanningApplication).filter(PlanningApplication.id == match.application_id).first()
    review = db.query(ReviewAction).filter(ReviewAction.match_id == match.id).first()
    return templates.TemplateResponse(
        "match_detail.html",
        {"request": request, "match": match, "application": app_row, "review": review},
    )
