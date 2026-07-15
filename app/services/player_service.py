"""Player service containing business logic for Player entity."""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app.schemas.player import PlayerCreate, PlayerRead
from app.repositories.player_repository import (
    get_player as repo_get_player,
    get_players as repo_get_players,
    create_player as repo_create_player,
)


def get_player_by_id(db: Session, player_id: int) -> Optional[PlayerRead]:
    player = repo_get_player(db, player_id)
    if player:
        return PlayerRead.from_orm(player)
    return None


def get_all_players(db: Session, skip: int = 0, limit: int = 100) -> List[PlayerRead]:
    players = repo_get_players(db, skip=skip, limit=limit)
    return [PlayerRead.from_orm(p) for p in players]


def create_player(db: Session, player_in: PlayerCreate) -> PlayerRead:
    player = repo_create_player(db, player_in.model_dump())
    return PlayerRead.from_orm(player)

# Update/delete functions could be added similarly
