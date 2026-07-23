from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class MatchStatus(str, Enum):
    SCHEDULED = "scheduled"
    LIVE = "live"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Match(Base):

    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tournament_id: Mapped[int] = mapped_column(
        ForeignKey("tournaments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    team1_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    team2_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    winner_id: Mapped[int | None] = mapped_column(
        ForeignKey("teams.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[MatchStatus] = mapped_column(
        SAEnum(MatchStatus, name="match_status"),
        nullable=False,
    )
    score_team1: Mapped[int | None] = mapped_column(Integer, nullable=True)
    score_team2: Mapped[int | None] = mapped_column(Integer, nullable=True)

    tournament: Mapped["Tournament"] = relationship(back_populates="matches")
    team1: Mapped["Team"] = relationship(
        back_populates="matches_as_team1",
        foreign_keys=[team1_id],
    )
    team2: Mapped["Team"] = relationship(
        back_populates="matches_as_team2",
        foreign_keys=[team2_id],
    )
    winner: Mapped["Team | None"] = relationship(
        back_populates="won_matches",
        foreign_keys=[winner_id],
    )

    def __repr__(self) -> str:
        return (
            f"Match(id={self.id!r}, tournament_id={self.tournament_id!r}, "
            f"team1_id={self.team1_id!r}, team2_id={self.team2_id!r}, status={self.status!r})"
        )
