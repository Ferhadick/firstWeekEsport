from __future__ import annotations

from sqlalchemy.orm import Session

from app.exceptions import AlreadyExistsException, BusinessValidationException, NotFoundException
from app.schemas.pagination import PaginatedResponse, validate_sort_params
from app.schemas.player import PlayerCreate, PlayerRead, PlayerUpdate
from app.repositories.player_repository import PlayerRepository
from app.repositories.team_repository import TeamRepository

VALID_SORT_COLUMNS = {
    "id", "nickname", "real_name", "country", "age", "role", "team_id",
}


def get_player_by_id(db: Session, player_id: int) -> PlayerRead:
    repo = PlayerRepository(db)
    player = repo.get(player_id)
    if not player:
        raise NotFoundException(f"Player with id {player_id} not found")
    return PlayerRead.model_validate(player)


def get_all_players(
    db: Session,
    *,
    page: int = 1,
    size: int = 10,
    sort_by: str | None = None,
    order: str | None = None,
) -> PaginatedResponse[PlayerRead]:
    if page < 1:
        raise BusinessValidationException("Page must be 1 or greater")
    if size < 1 or size > 100:
        raise BusinessValidationException("Size must be between 1 and 100")
    sort_by_normalized = sort_by.lower() if sort_by else None
    order_normalized = order.lower() if order else None
    validate_sort_params(sort_by_normalized, order_normalized, VALID_SORT_COLUMNS)
    repo = PlayerRepository(db)
    players, total = repo.get_all(
        page=page, size=size, sort_by=sort_by_normalized, order=order_normalized,
    )
    pages = (total + size - 1) // size if total else 0
    return PaginatedResponse(
        items=[PlayerRead.model_validate(p) for p in players],
        page=page,
        size=size,
        total=total,
        pages=pages,
    )


def create_player(db: Session, player_in: PlayerCreate) -> PlayerRead:
    repo = PlayerRepository(db)
    existing = repo.get_by_nickname(player_in.nickname)
    if existing:
        raise AlreadyExistsException(f"Player with nickname '{player_in.nickname}' already exists")
    if not TeamRepository(db).get(player_in.team_id):
        raise NotFoundException(f"Team with id {player_in.team_id} not found")
    player = repo.create(player_in.model_dump())
    return PlayerRead.model_validate(player)


def update_player(db: Session, player_id: int, player_update: PlayerUpdate) -> PlayerRead:
    repo = PlayerRepository(db)
    player = repo.get(player_id)
    if not player:
        raise NotFoundException(f"Player with id {player_id} not found")
    if player_update.nickname is not None and player_update.nickname != player.nickname:
        existing = repo.get_by_nickname(player_update.nickname)
        if existing:
            raise AlreadyExistsException(f"Player with nickname '{player_update.nickname}' already exists")
    if player_update.team_id is not None and player_update.team_id != player.team_id:
        if not TeamRepository(db).get(player_update.team_id):
            raise NotFoundException(f"Team with id {player_update.team_id} not found")
    updated = repo.update(player, player_update.model_dump(exclude_unset=True))
    return PlayerRead.model_validate(updated)


def delete_player(db: Session, player_id: int) -> None:
    repo = PlayerRepository(db)
    player = repo.get(player_id)
    if not player:
        raise NotFoundException(f"Player with id {player_id} not found")
    repo.delete(player)
