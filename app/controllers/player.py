"""Player controller (FastAPI router) handling HTTP requests for Player entity."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.player import PlayerCreate, PlayerRead
from app.services.player_service import (
    create_player as service_create_player,
    get_player_by_id as service_get_player,
    get_all_players as service_get_all_players,
)
from app.dependencies.database import get_db

router = APIRouter()

@router.post("/", response_model=PlayerRead, status_code=status.HTTP_201_CREATED)
def create_player_endpoint(player: PlayerCreate, db: Session = Depends(get_db)):
    return service_create_player(db, player)

@router.get("/{player_id}", response_model=PlayerRead)
def get_player_endpoint(player_id: int, db: Session = Depends(get_db)):
    player = service_get_player(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.get("/", response_model=list[PlayerRead])
def list_players_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service_get_all_players(db, skip=skip, limit=limit)
