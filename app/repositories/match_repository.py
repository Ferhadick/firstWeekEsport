"""Match repository handling database operations for Match entity."""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.match import Match


def get_match(db: Session, match_id: int) -> Optional[Match]:
    return db.query(Match).filter(Match.id == match_id).first()


def get_matches(db: Session, skip: int = 0, limit: int = 100) -> List[Match]:
    return db.query(Match).offset(skip).limit(limit).all()


def create_match(db: Session, match_data: dict) -> Match:
    match = Match(**match_data)
    db.add(match)
    db.commit()
    db.refresh(match)
    return match

# Additional CRUD functions can be added as needed
