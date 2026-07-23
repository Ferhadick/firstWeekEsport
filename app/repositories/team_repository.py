from __future__ import annotations

from app.models.team import Team
from app.repositories.base import BaseRepository


class TeamRepository(BaseRepository[Team]):
    model = Team

    def get_by_tag(self, tag: str) -> Team | None:
        return self._db.query(Team).filter(Team.tag == tag).first()
