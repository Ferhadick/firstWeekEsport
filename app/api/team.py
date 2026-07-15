"""Team API endpoints (Controller layer)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.team import TeamCreate, TeamRead, TeamUpdate
from app.services.team_service import (
    get_team_by_id,
    get_all_teams,
    create_team,
    update_team,
    delete_team,
)
from app.main import get_db

router = APIRouter()

@router.post("/", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
def create_team_endpoint(team: TeamCreate, db: Session = Depends(get_db)):
    return create_team(db, team)

@router.get("/{team_id}", response_model=TeamRead)
def get_team_endpoint(team_id: int, db: Session = Depends(get_db)):
    team = get_team_by_id(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.get("/", response_model=list[TeamRead])
def list_teams_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_teams(db, skip=skip, limit=limit)

@router.put("/{team_id}", response_model=TeamRead)
def update_team_endpoint(team_id: int, team_update: TeamUpdate, db: Session = Depends(get_db)):
    updated = update_team(db, team_id, team_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Team not found")
    return updated

@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team_endpoint(team_id: int, db: Session = Depends(get_db)):
    success = delete_team(db, team_id)
    if not success:
        raise HTTPException(status_code=404, detail="Team not found")
    return None
