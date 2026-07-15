"""Team service (business logic layer)."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.schemas.team import TeamCreate, TeamRead, TeamUpdate
from app.repositories.team_repository import (
    get_team as repo_get_team,
    get_teams as repo_get_teams,
    create_team as repo_create_team,
    update_team as repo_update_team,
    delete_team as repo_delete_team,
)


def get_team_by_id(db: Session, team_id: int) -> TeamRead | None:
    team = repo_get_team(db, team_id)
    if team:
        return TeamRead.model_validate(team)
    return None


def get_all_teams(db: Session, skip: int = 0, limit: int = 100) -> list[TeamRead]:
    teams = repo_get_teams(db, skip=skip, limit=limit)
    return [TeamRead.model_validate(team) for team in teams]


def create_team(db: Session, team_in: TeamCreate) -> TeamRead:
    team = repo_create_team(db, team_in.model_dump())
    return TeamRead.model_validate(team)


def update_team(db: Session, team_id: int, team_update: TeamUpdate) -> TeamRead | None:
    team = repo_get_team(db, team_id)
    if not team:
        return None
    updated = repo_update_team(db, team, team_update.model_dump(exclude_unset=True))
    return TeamRead.model_validate(updated)


def delete_team(db: Session, team_id: int) -> bool:
    team = repo_get_team(db, team_id)
    if not team:
        return False
    repo_delete_team(db, team)
    return True