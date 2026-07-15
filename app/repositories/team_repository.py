"""Team repository (data access layer)."""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.team import Team


def get_team(db: Session, team_id: int) -> Optional[Team]:
    return db.query(Team).filter(Team.id == team_id).first()


def get_teams(db: Session, skip: int = 0, limit: int = 100) -> List[Team]:
    return db.query(Team).offset(skip).limit(limit).all()


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
