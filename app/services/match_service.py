"""Match service containing business logic for Match entity."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.exceptions import BusinessValidationException, NotFoundException
from app.schemas.match import MatchCreate, MatchRead, MatchUpdate
from app.schemas.pagination import PaginatedResponse, validate_sort_params
from app.repositories.match_repository import (
    get_match as repo_get_match,
    get_matches as repo_get_matches,
    create_match as repo_create_match,
    update_match as repo_update_match,
    delete_match as repo_delete_match,
)

VALID_SORT_COLUMNS = {
    "id", "tournament_id", "team1_id", "team2_id", "winner_id",
    "scheduled_at", "status", "score_team1", "score_team2",
}


def get_match_by_id(db: Session, match_id: int) -> MatchRead:
    match = repo_get_match(db, match_id)
    if not match:
        raise NotFoundException(f"Match with id {match_id} not found")
    return MatchRead.model_validate(match)


def get_all_matches(
    db: Session,
    *,
    page: int = 1,
    size: int = 10,
    sort_by: str | None = None,
    order: str | None = None,
) -> PaginatedResponse[MatchRead]:
    if page < 1:
        raise BusinessValidationException("Page must be 1 or greater")
    if size < 1 or size > 100:
        raise BusinessValidationException("Size must be between 1 and 100")
    sort_by_normalized = sort_by.lower() if sort_by else None
    order_normalized = order.lower() if order else None
    validate_sort_params(sort_by_normalized, order_normalized, VALID_SORT_COLUMNS)
    matches, total = repo_get_matches(
        db, page=page, size=size, sort_by=sort_by_normalized, order=order_normalized,
    )
    pages = (total + size - 1) // size if total else 0
    return PaginatedResponse(
        items=[MatchRead.model_validate(m) for m in matches],
        page=page,
        size=size,
        total=total,
        pages=pages,
    )


def create_match(db: Session, match_in: MatchCreate) -> MatchRead:
    match = repo_create_match(db, match_in.model_dump())
    return MatchRead.model_validate(match)


def update_match(db: Session, match_id: int, match_update: MatchUpdate) -> MatchRead:
    match = repo_get_match(db, match_id)
    if not match:
        raise NotFoundException(f"Match with id {match_id} not found")
    updated = repo_update_match(db, match, match_update.model_dump(exclude_unset=True))
    return MatchRead.model_validate(updated)


def delete_match(db: Session, match_id: int) -> None:
    match = repo_get_match(db, match_id)
    if not match:
        raise NotFoundException(f"Match with id {match_id} not found")
    repo_delete_match(db, match)
