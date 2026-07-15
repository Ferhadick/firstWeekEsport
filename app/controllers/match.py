"""Match controller (FastAPI router) handling HTTP requests for Match entity."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.match import MatchCreate, MatchRead, MatchUpdate
from app.services.match_service import (
    create_match as service_create_match,
    get_match_by_id as service_get_match,
    get_all_matches as service_get_all_matches,
    update_match as service_update_match,
    delete_match as service_delete_match,
)
from app.dependencies.database import get_db

router = APIRouter()


@router.post("/", response_model=MatchRead, status_code=status.HTTP_201_CREATED)
def create_match_endpoint(match: MatchCreate, db: Session = Depends(get_db)):
    return service_create_match(db, match)


@router.get("/{match_id}", response_model=MatchRead)
def get_match_endpoint(match_id: int, db: Session = Depends(get_db)):
    return service_get_match(db, match_id)


@router.get("/", response_model=list[MatchRead])
def list_matches_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service_get_all_matches(db, skip=skip, limit=limit)


@router.put("/{match_id}", response_model=MatchRead)
def update_match_endpoint(match_id: int, match_update: MatchUpdate, db: Session = Depends(get_db)):
    return service_update_match(db, match_id, match_update)


@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match_endpoint(match_id: int, db: Session = Depends(get_db)):
    service_delete_match(db, match_id)
    return None
