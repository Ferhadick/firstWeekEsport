from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class MatchStatus(str, Enum):
    scheduled = "scheduled"
    live = "live"
    completed = "completed"
    cancelled = "cancelled"


class MatchBase(BaseModel):
    tournament_id: int = Field(
        ...,
        gt=0,
        description="The ID of the tournament this match belongs to",
        examples=[1],
    )
    team1_id: int = Field(
        ...,
        gt=0,
        description="The ID of the first team (must differ from team2_id)",
        examples=[1],
    )
    team2_id: int = Field(
        ...,
        gt=0,
        description="The ID of the second team (must differ from team1_id)",
        examples=[2],
    )
    scheduled_at: datetime = Field(
        ...,
        description="The scheduled date and time of the match (cannot be in the past)",
        examples=[datetime(2026, 7, 15, 18, 0, 0, tzinfo=timezone.utc)],
    )
    status: MatchStatus = Field(
        ...,
        description="Current status of the match",
        examples=[MatchStatus.scheduled],
    )
    winner_id: Optional[int] = Field(
        None,
        gt=0,
        description="The ID of the winning team (null until match concludes)",
        examples=[1],
    )
    score_team1: Optional[int] = Field(
        None,
        ge=0,
        description="Score for team1 (null until match is played)",
        examples=[3],
    )
    score_team2: Optional[int] = Field(
        None,
        ge=0,
        description="Score for team2 (null until match is played)",
        examples=[1],
    )

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_teams(self):
        if self.team1_id == self.team2_id:
            raise ValueError("team1_id and team2_id must be different")
        return self


class MatchCreate(MatchBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "tournament_id": 1,
                "team1_id": 1,
                "team2_id": 2,
                "scheduled_at": "2026-07-15T18:00:00Z",
                "status": "scheduled",
            }
        },
    )

    @model_validator(mode="after")
    def validate_scheduled_at(self):
        scheduled = (
            self.scheduled_at
            if self.scheduled_at.tzinfo is not None
            else self.scheduled_at.replace(tzinfo=timezone.utc)
        )
        if scheduled < datetime.now(timezone.utc):
            raise ValueError("scheduled_at cannot be in the past")
        return self


class MatchUpdate(BaseModel):
    tournament_id: Optional[int] = Field(
        None,
        gt=0,
        description="The ID of the tournament this match belongs to",
        examples=[2],
    )
    team1_id: Optional[int] = Field(
        None,
        gt=0,
        description="The ID of the first team (must differ from team2_id)",
        examples=[3],
    )
    team2_id: Optional[int] = Field(
        None,
        gt=0,
        description="The ID of the second team (must differ from team1_id)",
        examples=[4],
    )
    scheduled_at: Optional[datetime] = Field(
        None,
        description="The scheduled date and time of the match",
        examples=[datetime(2026, 8, 1, 20, 0, 0, tzinfo=timezone.utc)],
    )
    status: Optional[MatchStatus] = Field(
        None,
        description="Current status of the match",
        examples=[MatchStatus.live],
    )
    winner_id: Optional[int] = Field(
        None,
        gt=0,
        description="The ID of the winning team (null until match concludes)",
        examples=[1],
    )
    score_team1: Optional[int] = Field(
        None,
        ge=0,
        description="Score for team1",
        examples=[3],
    )
    score_team2: Optional[int] = Field(
        None,
        ge=0,
        description="Score for team2",
        examples=[2],
    )

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_teams(self):
        if self.team1_id is not None and self.team2_id is not None:
            if self.team1_id == self.team2_id:
                raise ValueError("team1_id and team2_id must be different")
        return self


class MatchRead(MatchBase):
    id: int = Field(
        ...,
        description="The unique identifier for the match",
        examples=[1],
    )
