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
from app.repositories.team_repository import get_team as repo_get_team
from app.repositories.tournament_repository import get_tournament as repo_get_tournament

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


def _ensure_team_exists(db: Session, team_id: int, label: str) -> None:
    if not repo_get_team(db, team_id):
        raise NotFoundException(f"{label} with id {team_id} not found")


def _ensure_tournament_exists(db: Session, tournament_id: int) -> None:
    if not repo_get_tournament(db, tournament_id):
        raise NotFoundException(f"Tournament with id {tournament_id} not found")


def create_match(db: Session, match_in: MatchCreate) -> MatchRead:
    _ensure_tournament_exists(db, match_in.tournament_id)
    _ensure_team_exists(db, match_in.team1_id, "Team1")
    _ensure_team_exists(db, match_in.team2_id, "Team2")
    match = repo_create_match(db, match_in.model_dump())
    return MatchRead.model_validate(match)


def update_match(db: Session, match_id: int, match_update: MatchUpdate) -> MatchRead:
    match = repo_get_match(db, match_id)
    if not match:
        raise NotFoundException(f"Match with id {match_id} not found")
    updates = match_update.model_dump(exclude_unset=True)
    if "tournament_id" in updates:
        _ensure_tournament_exists(db, updates["tournament_id"])
    if "team1_id" in updates:
        _ensure_team_exists(db, updates["team1_id"], "Team1")
    if "team2_id" in updates:
        _ensure_team_exists(db, updates["team2_id"], "Team2")
    if "winner_id" in updates and updates["winner_id"] is not None:
        _ensure_team_exists(db, updates["winner_id"], "Winner")
    updated = repo_update_match(db, match, updates)
    return MatchRead.model_validate(updated)


def delete_match(db: Session, match_id: int) -> None:
    match = repo_get_match(db, match_id)
    if not match:
        raise NotFoundException(f"Match with id {match_id} not found")
    repo_delete_match(db, match)
