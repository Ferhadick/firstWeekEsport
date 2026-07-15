"""Player repository handling database operations for Player entity."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.player import Player


def get_player(db: Session, player_id: int) -> Player | None:
    return db.query(Player).filter(Player.id == player_id).first()


def get_players(db: Session, skip: int = 0, limit: int = 100) -> list[Player]:
    return db.query(Player).offset(skip).limit(limit).all()


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