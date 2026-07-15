"""Team controller (FastAPI router) handling HTTP requests for Team entity."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.team import TeamCreate, TeamRead, TeamUpdate
from app.services.team_service import (
    create_team as service_create_team,
    get_team_by_id as service_get_team,
    get_all_teams as service_get_all_teams,
    update_team as service_update_team,
    delete_team as service_delete_team,
)
from app.dependencies.database import get_db

router = APIRouter()

@router.post("/", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
def create_team_endpoint(team: TeamCreate, db: Session = Depends(get_db)):
    """Create a new team."""
    return service_create_team(db, team)

@router.get("/{team_id}", response_model=TeamRead)
def get_team_endpoint(team_id: int, db: Session = Depends(get_db)):
    team = service_get_team(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.get("/", response_model=list[TeamRead])
def list_teams_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service_get_all_teams(db, skip=skip, limit=limit)

@router.put("/{team_id}", response_model=TeamRead)
def update_team_endpoint(team_id: int, team_update: TeamUpdate, db: Session = Depends(get_db)):
    updated = service_update_team(db, team_id, team_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Team not found")
    return updated

@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team_endpoint(team_id: int, db: Session = Depends(get_db)):
    success = service_delete_team(db, team_id)
    if not success:
        raise HTTPException(status_code=404, detail="Team not found")
    return None
