from __future__ import annotations

from datetime import date
from enum import Enum
from decimal import Decimal

from sqlalchemy import Date, Enum as SAEnum, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TournamentStatus(str, Enum):
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Tournament(Base):

    __tablename__ = "tournaments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    game: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    prize_pool: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[TournamentStatus] = mapped_column(
        SAEnum(TournamentStatus, name="tournament_status"),
        nullable=False,
    )

    matches: Mapped[list["Match"]] = relationship(
        back_populates="tournament",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"Tournament(id={self.id!r}, name={self.name!r}, "
            f"game={self.game!r}, status={self.status!r})"
        )
