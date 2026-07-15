"""Player controller (FastAPI router) handling HTTP requests for Player entity."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.schemas.pagination import PaginatedResponse
from app.schemas.player import PlayerCreate, PlayerRead, PlayerUpdate
from app.services.player_service import (
    create_player as service_create_player,
    get_player_by_id as service_get_player,
    get_all_players as service_get_all_players,
    update_player as service_update_player,
    delete_player as service_delete_player,
)
from app.dependencies.database import get_db

router = APIRouter()


@router.post("/", response_model=PlayerRead, status_code=status.HTTP_201_CREATED)
def create_player_endpoint(player: PlayerCreate, db: Session = Depends(get_db)):
    return service_create_player(db, player)


@router.get("/{player_id}", response_model=PlayerRead)
def get_player_endpoint(player_id: int, db: Session = Depends(get_db)):
    return service_get_player(db, player_id)


@router.get("/", response_model=PaginatedResponse[PlayerRead])
def list_players_endpoint(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    sort_by: str | None = Query(None),
    order: str | None = Query("asc"),
    db: Session = Depends(get_db),
):
    return service_get_all_players(db, page=page, size=size, sort_by=sort_by, order=order)


@router.put("/{player_id}", response_model=PlayerRead)
def update_player_endpoint(player_id: int, player_update: PlayerUpdate, db: Session = Depends(get_db)):
    return service_update_player(db, player_id, player_update)


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player_endpoint(player_id: int, db: Session = Depends(get_db)):
    service_delete_player(db, player_id)
    return None
