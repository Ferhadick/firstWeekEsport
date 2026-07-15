"""Match repository handling database operations for Match entity."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.match import Match


def get_match(db: Session, match_id: int) -> Match | None:
    return db.query(Match).filter(Match.id == match_id).first()


def get_matches(db: Session, skip: int = 0, limit: int = 100) -> list[Match]:
    return db.query(Match).offset(skip).limit(limit).all()


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