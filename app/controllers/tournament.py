"""Tournament controller (FastAPI router) handling HTTP requests for Tournament entity."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.schemas.pagination import PaginatedResponse
from app.schemas.tournament import TournamentCreate, TournamentRead, TournamentUpdate
from app.services.tournament_service import (
    create_tournament as service_create_tournament,
    get_tournament_by_id as service_get_tournament,
    get_all_tournaments as service_get_all_tournaments,
    update_tournament as service_update_tournament,
    delete_tournament as service_delete_tournament,
)
from app.dependencies.database import get_db

router = APIRouter(tags=["tournaments"])


@router.post(
    "/",
    response_model=TournamentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a tournament",
    description="Schedule a new tournament. Prize pool must be non-negative and end_date must be after start_date.",
)
def create_tournament_endpoint(tournament: TournamentCreate, db: Session = Depends(get_db)):
    return service_create_tournament(db, tournament)


@router.get(
    "/{tournament_id}",
    response_model=TournamentRead,
    summary="Get a tournament by ID",
    description="Retrieve a single tournament by its unique identifier.",
)
def get_tournament_endpoint(tournament_id: int, db: Session = Depends(get_db)):
    return service_get_tournament(db, tournament_id)


@router.get(
    "/",
    response_model=PaginatedResponse[TournamentRead],
    summary="List all tournaments",
    description="Paginated list of all tournaments with optional sorting by name, game, location, prize_pool, start_date, end_date, or status.",
)
def list_tournaments_endpoint(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    sort_by: str | None = Query(None),
    order: str | None = Query("asc"),
    db: Session = Depends(get_db),
):
    return service_get_all_tournaments(db, page=page, size=size, sort_by=sort_by, order=order)


@router.put(
    "/{tournament_id}",
    response_model=TournamentRead,
    summary="Update a tournament",
    description="Update one or more fields of an existing tournament.",
)
def update_tournament_endpoint(tournament_id: int, tournament_update: TournamentUpdate, db: Session = Depends(get_db)):
    return service_update_tournament(db, tournament_id, tournament_update)


@router.delete(
    "/{tournament_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a tournament",
    description="Permanently remove a tournament and all its matches.",
)
def delete_tournament_endpoint(tournament_id: int, db: Session = Depends(get_db)):
    service_delete_tournament(db, tournament_id)
    return None
