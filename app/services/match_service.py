"""Match service containing business logic for Match entity."""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app.schemas.match import MatchCreate, MatchRead
from app.repositories.match_repository import (
    get_match as repo_get_match,
    get_matches as repo_get_matches,
    create_match as repo_create_match,
)


def get_match_by_id(db: Session, match_id: int) -> Optional[MatchRead]:
    match = repo_get_match(db, match_id)
    if match:
        return MatchRead.from_orm(match)
    return None


def get_all_matches(db: Session, skip: int = 0, limit: int = 100) -> List[MatchRead]:
    matches = repo_get_matches(db, skip=skip, limit=limit)
    return [MatchRead.from_orm(m) for m in matches]


def create_match(db: Session, match_in: MatchCreate) -> MatchRead:
    match = repo_create_match(db, match_in.model_dump())
    return MatchRead.from_orm(match)

# Update/delete functions could be added similarly
