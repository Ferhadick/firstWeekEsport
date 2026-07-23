from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user, require_role
from app.dependencies.database import get_db
from app.models.user import User, UserRole
from app.schemas.pagination import PaginatedResponse
from app.schemas.tournament import TournamentCreate, TournamentRead, TournamentUpdate
from app.services.tournament_service import (
    create_tournament as service_create_tournament,
    get_tournament_by_id as service_get_tournament,
    get_all_tournaments as service_get_all_tournaments,
    update_tournament as service_update_tournament,
    delete_tournament as service_delete_tournament,
)

router = APIRouter(tags=["tournaments"])


@router.post(
    "/",
    response_model=TournamentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a tournament",
    description="Schedule a new tournament. Prize pool must be non-negative and end_date must be after start_date.",
)
def create_tournament_endpoint(
    tournament: TournamentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN])),
):
    return service_create_tournament(db, tournament)


@router.get(
    "/{tournament_id}",
    response_model=TournamentRead,
    summary="Get a tournament by ID",
    description="Retrieve a single tournament by its unique identifier.",
)
def get_tournament_endpoint(
    tournament_id: int = Path(..., description="The unique identifier of the tournament", examples=[1]),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service_get_tournament(db, tournament_id)


@router.get(
    "/",
    response_model=PaginatedResponse[TournamentRead],
    summary="List all tournaments",
    description="Paginated list of all tournaments with optional sorting by name, game, location, prize_pool, start_date, end_date, or status.",
)
def list_tournaments_endpoint(
    page: int = Query(1, ge=1, description="Page number (1-based)", examples=[1]),
    size: int = Query(10, ge=1, le=100, description="Number of items per page (1-100)", examples=[10]),
    sort_by: str | None = Query(None, description="Column to sort by (e.g. name, prize_pool)", examples=["name"]),
    order: str | None = Query("asc", description="Sort order: 'asc' or 'desc'", examples=["asc"]),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service_get_all_tournaments(db, page=page, size=size, sort_by=sort_by, order=order)


@router.put(
    "/{tournament_id}",
    response_model=TournamentRead,
    summary="Update a tournament",
    description="Update one or more fields of an existing tournament.",
)
def update_tournament_endpoint(
    tournament_id: int = Path(..., description="The unique identifier of the tournament to update", examples=[1]),
    tournament_update: TournamentUpdate = ...,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN])),
):
    return service_update_tournament(db, tournament_id, tournament_update)


@router.delete(
    "/{tournament_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a tournament",
    description="Permanently remove a tournament and all its matches.",
)
def delete_tournament_endpoint(
    tournament_id: int = Path(..., description="The unique identifier of the tournament to delete", examples=[1]),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN])),
):
    service_delete_tournament(db, tournament_id)
    return None
