"""Tournament controller (FastAPI router) handling HTTP requests for Tournament entity."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.tournament import TournamentCreate, TournamentRead
from app.services.tournament_service import (
    create_tournament as service_create_tournament,
    get_tournament_by_id as service_get_tournament,
    get_all_tournaments as service_get_all_tournaments,
)
from app.dependencies.database import get_db

router = APIRouter()

@router.post("/", response_model=TournamentRead, status_code=status.HTTP_201_CREATED)
def create_tournament_endpoint(tournament: TournamentCreate, db: Session = Depends(get_db)):
    return service_create_tournament(db, tournament)

@router.get("/{tournament_id}", response_model=TournamentRead)
def get_tournament_endpoint(tournament_id: int, db: Session = Depends(get_db)):
    tournament = service_get_tournament(db, tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return tournament

@router.get("/", response_model=list[TournamentRead])
def list_tournaments_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service_get_all_tournaments(db, skip=skip, limit=limit)
