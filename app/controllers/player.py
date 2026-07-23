from fastapi import APIRouter, Depends, Path, Query, status
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

router = APIRouter(tags=["players"])


@router.post(
    "/",
    response_model=PlayerRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a player",
    description="Add a new player to a team. Age must be between 13 and 60. The team must already exist.",
)
def create_player_endpoint(player: PlayerCreate, db: Session = Depends(get_db)):
    return service_create_player(db, player)


@router.get(
    "/{player_id}",
    response_model=PlayerRead,
    summary="Get a player by ID",
    description="Retrieve a single player by their unique identifier.",
)
def get_player_endpoint(
    player_id: int = Path(..., description="The unique identifier of the player", examples=[1]),
    db: Session = Depends(get_db),
):
    return service_get_player(db, player_id)


@router.get(
    "/",
    response_model=PaginatedResponse[PlayerRead],
    summary="List all players",
    description="Paginated list of all players with optional sorting by nickname, real_name, country, age, role, or team_id.",
)
def list_players_endpoint(
    page: int = Query(1, ge=1, description="Page number (1-based)", examples=[1]),
    size: int = Query(10, ge=1, le=100, description="Number of items per page (1-100)", examples=[10]),
    sort_by: str | None = Query(None, description="Column to sort by (e.g. nickname, age)", examples=["nickname"]),
    order: str | None = Query("asc", description="Sort order: 'asc' or 'desc'", examples=["asc"]),
    db: Session = Depends(get_db),
):
    return service_get_all_players(db, page=page, size=size, sort_by=sort_by, order=order)


@router.put(
    "/{player_id}",
    response_model=PlayerRead,
    summary="Update a player",
    description="Update one or more fields of an existing player.",
)
def update_player_endpoint(
    player_id: int = Path(..., description="The unique identifier of the player to update", examples=[1]),
    player_update: PlayerUpdate = ...,
    db: Session = Depends(get_db),
):
    return service_update_player(db, player_id, player_update)


@router.delete(
    "/{player_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a player",
    description="Permanently remove a player from the system.",
)
def delete_player_endpoint(
    player_id: int = Path(..., description="The unique identifier of the player to delete", examples=[1]),
    db: Session = Depends(get_db),
):
    service_delete_player(db, player_id)
    return None
