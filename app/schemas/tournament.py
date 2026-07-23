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
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="The tournament name (3-100 characters)",
        examples=["World Championship 2026"],
    )
    game: str = Field(
        ...,
        description="The video game being played in the tournament",
        examples=["League of Legends"],
    )
    location: str = Field(
        ...,
        max_length=255,
        description="The physical or online location of the tournament",
        examples=["Berlin, Germany"],
    )
    prize_pool: Decimal = Field(
        ...,
        ge=0,
        description="Total prize pool amount (must be non-negative)",
        examples=[Decimal("500000.00")],
    )
    start_date: date = Field(
        ...,
        description="The date the tournament starts",
        examples=[date(2026, 6, 1)],
    )
    end_date: date = Field(
        ...,
        description="The date the tournament ends (must be after start_date)",
        examples=[date(2026, 6, 15)],
    )
    status: TournamentStatus = Field(
        ...,
        description="Current status of the tournament",
        examples=[TournamentStatus.scheduled],
    )

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self


class TournamentCreate(TournamentBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "World Championship 2026",
                "game": "League of Legends",
                "location": "Berlin, Germany",
                "prize_pool": 500000.00,
                "start_date": "2026-06-01",
                "end_date": "2026-06-15",
                "status": "scheduled",
            }
        },
    )


class TournamentUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100,
        description="The tournament name (3-100 characters)",
        examples=["World Championship 2026"],
    )
    game: Optional[str] = Field(
        None,
        description="The video game being played in the tournament",
        examples=["Valorant"],
    )
    location: Optional[str] = Field(
        None,
        max_length=255,
        description="The physical or online location of the tournament",
        examples=["Paris, France"],
    )
    prize_pool: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Total prize pool amount (must be non-negative)",
        examples=[Decimal("750000.00")],
    )
    start_date: Optional[date] = Field(
        None,
        description="The date the tournament starts",
        examples=[date(2026, 7, 1)],
    )
    end_date: Optional[date] = Field(
        None,
        description="The date the tournament ends (must be after start_date)",
        examples=[date(2026, 7, 15)],
    )
    status: Optional[TournamentStatus] = Field(
        None,
        description="Current status of the tournament",
        examples=[TournamentStatus.active],
    )

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date is not None and self.end_date is not None:
            if self.end_date <= self.start_date:
                raise ValueError("end_date must be after start_date")
        return self


class TournamentRead(TournamentBase):
    id: int = Field(
        ...,
        description="The unique identifier for the tournament",
        examples=[1],
    )
