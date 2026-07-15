"""Team repository (data access layer)."""

from __future__ import annotations

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.models.team import Team


def get_team(db: Session, team_id: int) -> Team | None:
    return db.query(Team).filter(Team.id == team_id).first()


def get_team_by_tag(db: Session, tag: str) -> Team | None:
    return db.query(Team).filter(Team.tag == tag).first()


def get_teams(
    db: Session,
    *,
    page: int = 1,
    size: int = 10,
    sort_by: str | None = None,
    order: str | None = None,
) -> tuple[list[Team], int]:
    query = db.query(Team)
    if sort_by:
        sort_column = getattr(Team, sort_by)
        order_fn = asc if order == "asc" else desc
        query = query.order_by(order_fn(sort_column))
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return items, total


def create_team(db: Session, team_data: dict) -> Team:
    team = Team(**team_data)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def update_team(db: Session, team: Team, updates: dict) -> Team:
    for key, value in updates.items():
        if value is not None:
            setattr(team, key, value)
    db.commit()
    db.refresh(team)
    return team


def delete_team(db: Session, team: Team) -> None:
    db.delete(team)
    db.commit()