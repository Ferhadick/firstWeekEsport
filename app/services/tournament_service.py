"""Tournament service containing business logic for Tournament entity."""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app.schemas.tournament import TournamentCreate, TournamentRead
from app.repositories.tournament_repository import (
    get_tournament as repo_get_tournament,
    get_tournaments as repo_get_tournaments,
    create_tournament as repo_create_tournament,
)


def get_tournament_by_id(db: Session, tournament_id: int) -> Optional[TournamentRead]:
    tournament = repo_get_tournament(db, tournament_id)
    if tournament:
        return TournamentRead.from_orm(tournament)
    return None


def get_all_tournaments(db: Session, skip: int = 0, limit: int = 100) -> List[TournamentRead]:
    tournaments = repo_get_tournaments(db, skip=skip, limit=limit)
    return [TournamentRead.from_orm(t) for t in tournaments]


def create_tournament(db: Session, tournament_in: TournamentCreate) -> TournamentRead:
    tournament = repo_create_tournament(db, tournament_in.model_dump())
    return TournamentRead.from_orm(tournament)

# Update and delete methods would follow similar pattern
