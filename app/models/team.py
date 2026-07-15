"""Team domain model."""

from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Team(Base):
    """Represents a professional esports team."""

    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    tag: Mapped[str] = mapped_column(String(16), nullable=False, unique=True, index=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    founded_year: Mapped[int] = mapped_column(Integer, nullable=False)
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    players: Mapped[list["Player"]] = relationship(
        back_populates="team",
        cascade="all, delete-orphan",
    )
    matches_as_team1: Mapped[list["Match"]] = relationship(
        back_populates="team1",
        foreign_keys="Match.team1_id",
    )
    matches_as_team2: Mapped[list["Match"]] = relationship(
        back_populates="team2",
        foreign_keys="Match.team2_id",
    )
    won_matches: Mapped[list["Match"]] = relationship(
        back_populates="winner",
        foreign_keys="Match.winner_id",
    )

    def __repr__(self) -> str:
        return f"Team(id={self.id!r}, name={self.name!r}, tag={self.tag!r})"
