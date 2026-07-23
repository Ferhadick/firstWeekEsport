from __future__ import annotations

from sqlalchemy.orm import Session

from app.exceptions import BusinessValidationException, NotFoundException
from app.schemas.pagination import PaginatedResponse, validate_sort_params
from app.schemas.tournament import TournamentCreate, TournamentRead, TournamentUpdate
from app.repositories.tournament_repository import TournamentRepository

VALID_SORT_COLUMNS = {
    "id", "name", "game", "location", "prize_pool", "start_date", "end_date", "status",
}


def get_tournament_by_id(db: Session, tournament_id: int) -> TournamentRead:
    repo = TournamentRepository(db)
    tournament = repo.get(tournament_id)
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
    repo = TournamentRepository(db)
    tournaments, total = repo.get_all(
        page=page, size=size, sort_by=sort_by_normalized, order=order_normalized,
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
    repo = TournamentRepository(db)
    tournament = repo.create(tournament_in.model_dump())
    return TournamentRead.model_validate(tournament)


def update_tournament(db: Session, tournament_id: int, tournament_update: TournamentUpdate) -> TournamentRead:
    repo = TournamentRepository(db)
    tournament = repo.get(tournament_id)
    if not tournament:
        raise NotFoundException(f"Tournament with id {tournament_id} not found")
    updated = repo.update(tournament, tournament_update.model_dump(exclude_unset=True))
    return TournamentRead.model_validate(updated)


def delete_tournament(db: Session, tournament_id: int) -> None:
    repo = TournamentRepository(db)
    tournament = repo.get(tournament_id)
    if not tournament:
        raise NotFoundException(f"Tournament with id {tournament_id} not found")
    repo.delete(tournament)
