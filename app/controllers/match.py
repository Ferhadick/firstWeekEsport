from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user, require_role
from app.dependencies.database import get_db
from app.models.user import User, UserRole
from app.schemas.match import MatchCreate, MatchRead, MatchUpdate
from app.schemas.pagination import PaginatedResponse
from app.services.match_service import (
    create_match as service_create_match,
    get_match_by_id as service_get_match,
    get_all_matches as service_get_all_matches,
    update_match as service_update_match,
    delete_match as service_delete_match,
)

router = APIRouter(tags=["matches"])


@router.post(
    "/",
    response_model=MatchRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a match",
    description="Schedule a new match. The referenced tournament and both teams must already exist. "
    "Team1 and Team2 must be different, and the scheduled time cannot be in the past.",
)
def create_match_endpoint(
    match: MatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN])),
):
    return service_create_match(db, match)


@router.get(
    "/{match_id}",
    response_model=MatchRead,
    summary="Get a match by ID",
    description="Retrieve a single match by its unique identifier.",
)
def get_match_endpoint(
    match_id: int = Path(..., description="The unique identifier of the match", examples=[1]),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service_get_match(db, match_id)


@router.get(
    "/",
    response_model=PaginatedResponse[MatchRead],
    summary="List all matches",
    description="Paginated list of all matches with optional sorting by id, tournament_id, team1_id, team2_id, "
    "winner_id, scheduled_at, status, score_team1, or score_team2.",
)
def list_matches_endpoint(
    page: int = Query(1, ge=1, description="Page number (1-based)", examples=[1]),
    size: int = Query(10, ge=1, le=100, description="Number of items per page (1-100)", examples=[10]),
    sort_by: str | None = Query(None, description="Column to sort by (e.g. status, scheduled_at)", examples=["scheduled_at"]),
    order: str | None = Query("asc", description="Sort order: 'asc' or 'desc'", examples=["asc"]),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service_get_all_matches(db, page=page, size=size, sort_by=sort_by, order=order)


@router.put(
    "/{match_id}",
    response_model=MatchRead,
    summary="Update a match",
    description="Update one or more fields of an existing match. Referenced teams and tournament are validated.",
)
def update_match_endpoint(
    match_id: int = Path(..., description="The unique identifier of the match to update", examples=[1]),
    match_update: MatchUpdate = ...,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN])),
):
    return service_update_match(db, match_id, match_update)


@router.delete(
    "/{match_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a match",
    description="Permanently remove a match from the system.",
)
def delete_match_endpoint(
    match_id: int = Path(..., description="The unique identifier of the match to delete", examples=[1]),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN])),
):
    service_delete_match(db, match_id)
    return None
