from __future__ import annotations

from app.models.player import Player
from app.repositories.base import BaseRepository


class PlayerRepository(BaseRepository[Player]):
    model = Player

    def get_by_nickname(self, nickname: str) -> Player | None:
        return self._db.query(Player).filter(Player.nickname == nickname).first()
