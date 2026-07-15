"""DTOs (Pydantic schemas) for Tournament entity."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TournamentStatus(str, Enum):
    scheduled = "scheduled"
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


class TournamentBase(BaseModel):
    name: str = Field(..., max_length=255)
    game: str = Field(..., max_length=255)
    location: str = Field(..., max_length=255)
    prize_pool: Decimal = Field(...)
    start_date: date
    end_date: date
    status: TournamentStatus

    model_config = ConfigDict(from_attributes=True)


class TournamentCreate(TournamentBase):
    pass


class TournamentUpdate(BaseModel):
    name: Optional[str] = None
    game: Optional[str] = None
    location: Optional[str] = None
    prize_pool: Optional[Decimal] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[TournamentStatus] = None

    model_config = ConfigDict(from_attributes=True)


class TournamentRead(TournamentBase):
    id: int
