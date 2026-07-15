"""Tournament service containing business logic for Tournament entity."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.schemas.tournament import TournamentCreate, TournamentRead, TournamentUpdate
from app.repositories.tournament_repository import (
    get_tournament as repo_get_tournament,
    get_tournaments as repo_get_tournaments,
    create_tournament as repo_create_tournament,
    update_tournament as repo_update_tournament,
    delete_tournament as repo_delete_tournament,
)


def get_tournament_by_id(db: Session, tournament_id: int) -> TournamentRead | None:
    tournament = repo_get_tournament(db, tournament_id)
    if tournament:
        return TournamentRead.model_validate(tournament)
    return None


def get_all_tournaments(db: Session, skip: int = 0, limit: int = 100) -> list[TournamentRead]:
    tournaments = repo_get_tournaments(db, skip=skip, limit=limit)
    return [TournamentRead.model_validate(t) for t in tournaments]


def create_tournament(db: Session, tournament_in: TournamentCreate) -> TournamentRead:
    tournament = repo_create_tournament(db, tournament_in.model_dump())
    return TournamentRead.model_validate(tournament)


def update_tournament(db: Session, tournament_id: int, tournament_update: TournamentUpdate) -> TournamentRead | None:
    tournament = repo_get_tournament(db, tournament_id)
    if not tournament:
        return None
    updated = repo_update_tournament(db, tournament, tournament_update.model_dump(exclude_unset=True))
    return TournamentRead.model_validate(updated)


def delete_tournament(db: Session, tournament_id: int) -> bool:
    tournament = repo_get_tournament(db, tournament_id)
    if not tournament:
        return False
    repo_delete_tournament(db, tournament)
    return True