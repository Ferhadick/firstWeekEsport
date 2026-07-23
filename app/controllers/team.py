from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user, require_role
from app.dependencies.database import get_db
from app.models.user import User, UserRole
from app.schemas.pagination import PaginatedResponse
from app.schemas.team import TeamCreate, TeamRead, TeamUpdate
from app.services.team_service import (
    create_team as service_create_team,
    get_team_by_id as service_get_team,
    get_all_teams as service_get_all_teams,
    update_team as service_update_team,
    delete_team as service_delete_team,
)

router = APIRouter(tags=["teams"])


@router.post(
    "/",
    response_model=TeamRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a team",
    description="Register a new esports team. The tag must be uppercase and 2-5 characters.",
)
def create_team_endpoint(
    team: TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN])),
):
    return service_create_team(db, team)


@router.get(
    "/{team_id}",
    response_model=TeamRead,
    summary="Get a team by ID",
    description="Retrieve a single team by its unique identifier.",
)
def get_team_endpoint(
    team_id: int = Path(..., description="The unique identifier of the team", examples=[1]),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service_get_team(db, team_id)


@router.get(
    "/",
    response_model=PaginatedResponse[TeamRead],
    summary="List all teams",
    description="Paginated list of all teams with optional sorting by name, tag, country, founded_year, or logo_url.",
)
def list_teams_endpoint(
    page: int = Query(1, ge=1, description="Page number (1-based)", examples=[1]),
    size: int = Query(10, ge=1, le=100, description="Number of items per page (1-100)", examples=[10]),
    sort_by: str | None = Query(None, description="Column to sort by (e.g. name, founded_year)", examples=["name"]),
    order: str | None = Query("asc", description="Sort order: 'asc' or 'desc'", examples=["asc"]),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service_get_all_teams(db, page=page, size=size, sort_by=sort_by, order=order)


@router.put(
    "/{team_id}",
    response_model=TeamRead,
    summary="Update a team",
    description="Update one or more fields of an existing team.",
)
def update_team_endpoint(
    team_id: int = Path(..., description="The unique identifier of the team to update", examples=[1]),
    team_update: TeamUpdate = ...,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN])),
):
    return service_update_team(db, team_id, team_update)


@router.delete(
    "/{team_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a team",
    description="Permanently remove a team and all its players.",
)
def delete_team_endpoint(
    team_id: int = Path(..., description="The unique identifier of the team to delete", examples=[1]),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN])),
):
    service_delete_team(db, team_id)
    return None
