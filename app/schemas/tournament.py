"""DTOs (Pydantic schemas) for Tournament entity."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class TournamentBase(BaseModel):
    name: str = Field(..., max_length=255)
    game: str = Field(..., max_length=255)
    location: str = Field(..., max_length=255)
    prize_pool: Decimal = Field(...)
    start_date: date
    end_date: date
    status: str = Field(...)

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
    status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class TournamentRead(TournamentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
