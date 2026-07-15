"""Tournament repository handling database operations for Tournament entity."""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.tournament import Tournament


def get_tournament(db: Session, tournament_id: int) -> Optional[Tournament]:
    return db.query(Tournament).filter(Tournament.id == tournament_id).first()


def get_tournaments(db: Session, skip: int = 0, limit: int = 100) -> List[Tournament]:
    return db.query(Tournament).offset(skip).limit(limit).all()


def create_tournament(db: Session, tournament_data: dict) -> Tournament:
    tournament = Tournament(**tournament_data)
    db.add(tournament)
    db.commit()
    db.refresh(tournament)
    return tournament

# Additional CRUD methods could be added similarly
