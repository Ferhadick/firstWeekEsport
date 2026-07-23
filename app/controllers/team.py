

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.schemas.pagination import PaginatedResponse
from app.schemas.team import TeamCreate, TeamRead, TeamUpdate
from app.services.team_service import (
    create_team as service_create_team,
    get_team_by_id as service_get_team,
    get_all_teams as service_get_all_teams,
    update_team as service_update_team,
    delete_team as service_delete_team,
)
from app.dependencies.database import get_db

router = APIRouter(tags=["teams"])

@router.post(
    "/",
    response_model=TeamRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a team",
    description="Register a new esports team. The tag must be uppercase and 2-5 characters.",
)
def create_team_endpoint(team: TeamCreate, db: Session = Depends(get_db)):
    return service_create_team(db, team)

@router.get(
    "/{team_id}",
    response_model=TeamRead,
    summary="Get a team by ID",
    description="Retrieve a single team by its unique identifier.",
)
def get_team_endpoint(team_id: int, db: Session = Depends(get_db)):
    return service_get_team(db, team_id)

@router.get(
    "/",
    response_model=PaginatedResponse[TeamRead],
    summary="List all teams",
    description="Paginated list of all teams with optional sorting by name, tag, country, founded_year, or logo_url.",
)
def list_teams_endpoint(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    sort_by: str | None = Query(None),
    order: str | None = Query("asc"),
    db: Session = Depends(get_db),
):
    return service_get_all_teams(db, page=page, size=size, sort_by=sort_by, order=order)

@router.put(
    "/{team_id}",
    response_model=TeamRead,
    summary="Update a team",
    description="Update one or more fields of an existing team.",
)
def update_team_endpoint(team_id: int, team_update: TeamUpdate, db: Session = Depends(get_db)):
    return service_update_team(db, team_id, team_update)

@router.delete(
    "/{team_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a team",
    description="Permanently remove a team and all its players.",
)
def delete_team_endpoint(team_id: int, db: Session = Depends(get_db)):
    service_delete_team(db, team_id)
    return None
