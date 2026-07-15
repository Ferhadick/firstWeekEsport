"""Match controller (FastAPI router) handling HTTP requests for Match entity."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.match import MatchCreate, MatchRead
from app.services.match_service import (
    create_match as service_create_match,
    get_match_by_id as service_get_match,
    get_all_matches as service_get_all_matches,
)
from app.dependencies.database import get_db

router = APIRouter()

@router.post("/", response_model=MatchRead, status_code=status.HTTP_201_CREATED)
def create_match_endpoint(match: MatchCreate, db: Session = Depends(get_db)):
    return service_create_match(db, match)

@router.get("/{match_id}", response_model=MatchRead)
def get_match_endpoint(match_id: int, db: Session = Depends(get_db)):
    match = service_get_match(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@router.get("/", response_model=list[MatchRead])
def list_matches_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service_get_all_matches(db, skip=skip, limit=limit)
