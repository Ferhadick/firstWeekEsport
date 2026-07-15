"""Tournament repository handling database operations for Tournament entity."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.tournament import Tournament


def get_tournament(db: Session, tournament_id: int) -> Tournament | None:
    return db.query(Tournament).filter(Tournament.id == tournament_id).first()


def get_tournament_by_name(db: Session, name: str) -> Tournament | None:
    return db.query(Tournament).filter(Tournament.name == name).first()


def get_tournaments(db: Session, skip: int = 0, limit: int = 100) -> list[Tournament]:
    return db.query(Tournament).offset(skip).limit(limit).all()


def create_tournament(db: Session, tournament_data: dict) -> Tournament:
    tournament = Tournament(**tournament_data)
    db.add(tournament)
    db.commit()
    db.refresh(tournament)
    return tournament


def update_tournament(db: Session, tournament: Tournament, updates: dict) -> Tournament:
    for key, value in updates.items():
        if value is not None:
            setattr(tournament, key, value)
    db.commit()
    db.refresh(tournament)
    return tournament


def delete_tournament(db: Session, tournament: Tournament) -> None:
    db.delete(tournament)
    db.commit()