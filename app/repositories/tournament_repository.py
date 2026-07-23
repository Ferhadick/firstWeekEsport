

from __future__ import annotations

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.models.tournament import Tournament


def get_tournament(db: Session, tournament_id: int) -> Tournament | None:
    return db.query(Tournament).filter(Tournament.id == tournament_id).first()


def get_tournament_by_name(db: Session, name: str) -> Tournament | None:
    return db.query(Tournament).filter(Tournament.name == name).first()


def get_tournaments(
    db: Session,
    *,
    page: int = 1,
    size: int = 10,
    sort_by: str | None = None,
    order: str | None = None,
) -> tuple[list[Tournament], int]:
    query = db.query(Tournament)
    if sort_by:
        sort_column = getattr(Tournament, sort_by)
        order_fn = asc if order == "asc" else desc
        query = query.order_by(order_fn(sort_column))
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return items, total


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