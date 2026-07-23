

from __future__ import annotations

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.models.player import Player


def get_player(db: Session, player_id: int) -> Player | None:
    return db.query(Player).filter(Player.id == player_id).first()


def get_player_by_nickname(db: Session, nickname: str) -> Player | None:
    return db.query(Player).filter(Player.nickname == nickname).first()


def get_players(
    db: Session,
    *,
    page: int = 1,
    size: int = 10,
    sort_by: str | None = None,
    order: str | None = None,
) -> tuple[list[Player], int]:
    query = db.query(Player)
    if sort_by:
        sort_column = getattr(Player, sort_by)
        order_fn = asc if order == "asc" else desc
        query = query.order_by(order_fn(sort_column))
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return items, total


def create_player(db: Session, player_data: dict) -> Player:
    player = Player(**player_data)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def update_player(db: Session, player: Player, updates: dict) -> Player:
    for key, value in updates.items():
        if value is not None:
            setattr(player, key, value)
    db.commit()
    db.refresh(player)
    return player


def delete_player(db: Session, player: Player) -> None:
    db.delete(player)
    db.commit()