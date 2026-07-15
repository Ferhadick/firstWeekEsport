"""Player repository handling database operations for Player entity."""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.player import Player


def get_player(db: Session, player_id: int) -> Optional[Player]:
    return db.query(Player).filter(Player.id == player_id).first()


def get_players(db: Session, skip: int = 0, limit: int = 100) -> List[Player]:
    return db.query(Player).offset(skip).limit(limit).all()


def create_player(db: Session, player_data: dict) -> Player:
    player = Player(**player_data)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player

# Additional methods can be added as needed
