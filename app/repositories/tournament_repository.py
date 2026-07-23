from __future__ import annotations

from app.models.tournament import Tournament
from app.repositories.base import BaseRepository


class TournamentRepository(BaseRepository[Tournament]):
    model = Tournament

    def get_by_name(self, name: str) -> Tournament | None:
        return self._db.query(Tournament).filter(Tournament.name == name).first()
