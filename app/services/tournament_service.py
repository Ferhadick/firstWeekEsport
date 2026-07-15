"""Tournament service containing business logic for Tournament entity."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.exceptions import BusinessValidationException, NotFoundException
from app.schemas.pagination import PaginatedResponse, validate_sort_params
from app.schemas.tournament import TournamentCreate, TournamentRead, TournamentUpdate
from app.repositories.tournament_repository import (
    get_tournament as repo_get_tournament,
    get_tournaments as repo_get_tournaments,
    create_tournament as repo_create_tournament,
    update_tournament as repo_update_tournament,
    delete_tournament as repo_delete_tournament,
)

VALID_SORT_COLUMNS = {
    "id", "name", "game", "location", "prize_pool", "start_date", "end_date", "status",
}


def get_tournament_by_id(db: Session, tournament_id: int) -> TournamentRead:
    tournament = repo_get_tournament(db, tournament_id)
    if not tournament:
        raise NotFoundException(f"Tournament with id {tournament_id} not found")
    return TournamentRead.model_validate(tournament)


def get_all_tournaments(
    db: Session,
    *,
    page: int = 1,
    size: int = 10,
    sort_by: str | None = None,
    order: str | None = None,
) -> PaginatedResponse[TournamentRead]:
    if page < 1:
        raise BusinessValidationException("Page must be 1 or greater")
    if size < 1 or size > 100:
        raise BusinessValidationException("Size must be between 1 and 100")
    sort_by_normalized = sort_by.lower() if sort_by else None
    order_normalized = order.lower() if order else None
    validate_sort_params(sort_by_normalized, order_normalized, VALID_SORT_COLUMNS)
    tournaments, total = repo_get_tournaments(
        db, page=page, size=size, sort_by=sort_by_normalized, order=order_normalized,
    )
    pages = (total + size - 1) // size if total else 0
    return PaginatedResponse(
        items=[TournamentRead.model_validate(t) for t in tournaments],
        page=page,
        size=size,
        total=total,
        pages=pages,
    )


def create_tournament(db: Session, tournament_in: TournamentCreate) -> TournamentRead:
    tournament = repo_create_tournament(db, tournament_in.model_dump())
    return TournamentRead.model_validate(tournament)


def update_tournament(db: Session, tournament_id: int, tournament_update: TournamentUpdate) -> TournamentRead:
    tournament = repo_get_tournament(db, tournament_id)
    if not tournament:
        raise NotFoundException(f"Tournament with id {tournament_id} not found")
    updated = repo_update_tournament(db, tournament, tournament_update.model_dump(exclude_unset=True))
    return TournamentRead.model_validate(updated)


def delete_tournament(db: Session, tournament_id: int) -> None:
    tournament = repo_get_tournament(db, tournament_id)
    if not tournament:
        raise NotFoundException(f"Tournament with id {tournament_id} not found")
    repo_delete_tournament(db, tournament)
