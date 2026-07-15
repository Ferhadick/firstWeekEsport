"""Team service (business logic layer)."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.exceptions import AlreadyExistsException, BusinessValidationException, NotFoundException
from app.schemas.pagination import PaginatedResponse, validate_sort_params
from app.schemas.team import TeamCreate, TeamRead, TeamUpdate
from app.repositories.team_repository import (
    get_team as repo_get_team,
    get_teams as repo_get_teams,
    create_team as repo_create_team,
    update_team as repo_update_team,
    delete_team as repo_delete_team,
    get_team_by_tag as repo_get_team_by_tag,
)

VALID_SORT_COLUMNS = {
    "id", "name", "tag", "country", "founded_year", "logo_url",
}


def get_team_by_id(db: Session, team_id: int) -> TeamRead:
    team = repo_get_team(db, team_id)
    if not team:
        raise NotFoundException(f"Team with id {team_id} not found")
    return TeamRead.model_validate(team)


def get_all_teams(
    db: Session,
    *,
    page: int = 1,
    size: int = 10,
    sort_by: str | None = None,
    order: str | None = None,
) -> PaginatedResponse[TeamRead]:
    if page < 1:
        raise BusinessValidationException("Page must be 1 or greater")
    if size < 1 or size > 100:
        raise BusinessValidationException("Size must be between 1 and 100")
    sort_by_normalized = sort_by.lower() if sort_by else None
    order_normalized = order.lower() if order else None
    validate_sort_params(sort_by_normalized, order_normalized, VALID_SORT_COLUMNS)
    teams, total = repo_get_teams(
        db, page=page, size=size, sort_by=sort_by_normalized, order=order_normalized,
    )
    pages = (total + size - 1) // size if total else 0
    return PaginatedResponse(
        items=[TeamRead.model_validate(t) for t in teams],
        page=page,
        size=size,
        total=total,
        pages=pages,
    )


def create_team(db: Session, team_in: TeamCreate) -> TeamRead:
    existing = repo_get_team_by_tag(db, team_in.tag)
    if existing:
        raise AlreadyExistsException(f"Team with tag '{team_in.tag}' already exists")
    team = repo_create_team(db, team_in.model_dump())
    return TeamRead.model_validate(team)


def update_team(db: Session, team_id: int, team_update: TeamUpdate) -> TeamRead:
    team = repo_get_team(db, team_id)
    if not team:
        raise NotFoundException(f"Team with id {team_id} not found")
    if team_update.tag is not None and team_update.tag != team.tag:
        existing = repo_get_team_by_tag(db, team_update.tag)
        if existing:
            raise AlreadyExistsException(f"Team with tag '{team_update.tag}' already exists")
    updated = repo_update_team(db, team, team_update.model_dump(exclude_unset=True))
    return TeamRead.model_validate(updated)


def delete_team(db: Session, team_id: int) -> None:
    team = repo_get_team(db, team_id)
    if not team:
        raise NotFoundException(f"Team with id {team_id} not found")
    repo_delete_team(db, team)
