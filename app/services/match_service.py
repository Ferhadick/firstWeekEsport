"""Match service containing business logic for Match entity."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.schemas.match import MatchCreate, MatchRead, MatchUpdate
from app.repositories.match_repository import (
    get_match as repo_get_match,
    get_matches as repo_get_matches,
    create_match as repo_create_match,
    update_match as repo_update_match,
    delete_match as repo_delete_match,
)


def get_match_by_id(db: Session, match_id: int) -> MatchRead | None:
    match = repo_get_match(db, match_id)
    if match:
        return MatchRead.model_validate(match)
    return None


def get_all_matches(db: Session, skip: int = 0, limit: int = 100) -> list[MatchRead]:
    matches = repo_get_matches(db, skip=skip, limit=limit)
    return [MatchRead.model_validate(m) for m in matches]


def create_match(db: Session, match_in: MatchCreate) -> MatchRead:
    match = repo_create_match(db, match_in.model_dump())
    return MatchRead.model_validate(match)


def update_match(db: Session, match_id: int, match_update: MatchUpdate) -> MatchRead | None:
    match = repo_get_match(db, match_id)
    if not match:
        return None
    updated = repo_update_match(db, match, match_update.model_dump(exclude_unset=True))
    return MatchRead.model_validate(updated)


def delete_match(db: Session, match_id: int) -> bool:
    match = repo_get_match(db, match_id)
    if not match:
        return False
    repo_delete_match(db, match)
    return True