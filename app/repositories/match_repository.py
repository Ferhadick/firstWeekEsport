

from __future__ import annotations

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.models.match import Match


def get_match(db: Session, match_id: int) -> Match | None:
    return db.query(Match).filter(Match.id == match_id).first()


def get_matches(
    db: Session,
    *,
    page: int = 1,
    size: int = 10,
    sort_by: str | None = None,
    order: str | None = None,
) -> tuple[list[Match], int]:
    query = db.query(Match)
    if sort_by:
        sort_column = getattr(Match, sort_by)
        order_fn = asc if order == "asc" else desc
        query = query.order_by(order_fn(sort_column))
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return items, total


def create_match(db: Session, match_data: dict) -> Match:
    match = Match(**match_data)
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


def update_match(db: Session, match: Match, updates: dict) -> Match:
    for key, value in updates.items():
        if value is not None:
            setattr(match, key, value)
    db.commit()
    db.refresh(match)
    return match


def delete_match(db: Session, match: Match) -> None:
    db.delete(match)
    db.commit()