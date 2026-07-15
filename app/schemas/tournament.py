"""DTOs (Pydantic schemas) for Tournament entity."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class TournamentStatus(str, Enum):
    scheduled = "scheduled"
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


class TournamentBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    game: str = Field(...)
    location: str = Field(..., max_length=255)
    prize_pool: Decimal = Field(..., ge=0)
    start_date: date
    end_date: date
    status: TournamentStatus

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self


class TournamentCreate(TournamentBase):
    pass


class TournamentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    game: Optional[str] = None
    location: Optional[str] = None
    prize_pool: Optional[Decimal] = Field(None, ge=0)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[TournamentStatus] = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date is not None and self.end_date is not None:
            if self.end_date <= self.start_date:
                raise ValueError("end_date must be after start_date")
        return self


class TournamentRead(TournamentBase):
    id: int
