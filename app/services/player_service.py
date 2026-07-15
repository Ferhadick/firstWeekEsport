"""Player service containing business logic for Player entity."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.exceptions import AlreadyExistsException, NotFoundException
from app.schemas.player import PlayerCreate, PlayerRead, PlayerUpdate
from app.repositories.player_repository import (
    get_player as repo_get_player,
    get_players as repo_get_players,
    create_player as repo_create_player,
    update_player as repo_update_player,
    delete_player as repo_delete_player,
    get_player_by_nickname as repo_get_player_by_nickname,
)


def get_player_by_id(db: Session, player_id: int) -> PlayerRead:
    player = repo_get_player(db, player_id)
    if not player:
        raise NotFoundException(f"Player with id {player_id} not found")
    return PlayerRead.model_validate(player)


def get_all_players(db: Session, skip: int = 0, limit: int = 100) -> list[PlayerRead]:
    players = repo_get_players(db, skip=skip, limit=limit)
    return [PlayerRead.model_validate(p) for p in players]


def create_player(db: Session, player_in: PlayerCreate) -> PlayerRead:
    existing = repo_get_player_by_nickname(db, player_in.nickname)
    if existing:
        raise AlreadyExistsException(f"Player with nickname '{player_in.nickname}' already exists")
    player = repo_create_player(db, player_in.model_dump())
    return PlayerRead.model_validate(player)


def update_player(db: Session, player_id: int, player_update: PlayerUpdate) -> PlayerRead:
    player = repo_get_player(db, player_id)
    if not player:
        raise NotFoundException(f"Player with id {player_id} not found")
    if player_update.nickname is not None and player_update.nickname != player.nickname:
        existing = repo_get_player_by_nickname(db, player_update.nickname)
        if existing:
            raise AlreadyExistsException(f"Player with nickname '{player_update.nickname}' already exists")
    updated = repo_update_player(db, player, player_update.model_dump(exclude_unset=True))
    return PlayerRead.model_validate(updated)


def delete_player(db: Session, player_id: int) -> None:
    player = repo_get_player(db, player_id)
    if not player:
        raise NotFoundException(f"Player with id {player_id} not found")
    repo_delete_player(db, player)
