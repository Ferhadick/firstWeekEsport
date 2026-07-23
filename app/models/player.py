from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Player(Base):

    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nickname: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    real_name: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    team: Mapped["Team"] = relationship(back_populates="players")

    def __repr__(self) -> str:
        return f"Player(id={self.id!r}, nickname={self.nickname!r}, team_id={self.team_id!r})"
