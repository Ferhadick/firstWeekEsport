

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
    tournament_id: int
    team1_id: int
    team2_id: int
    scheduled_at: datetime
    status: MatchStatus
    winner_id: Optional[int] = None
    score_team1: Optional[int] = Field(None, ge=0)
    score_team2: Optional[int] = Field(None, ge=0)

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_teams(self):
        if self.team1_id == self.team2_id:
            raise ValueError("team1_id and team2_id must be different")
        return self


class MatchCreate(MatchBase):
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
    tournament_id: Optional[int] = None
    team1_id: Optional[int] = None
    team2_id: Optional[int] = None
    scheduled_at: Optional[datetime] = None
    status: Optional[MatchStatus] = None
    winner_id: Optional[int] = None
    score_team1: Optional[int] = Field(None, ge=0)
    score_team2: Optional[int] = Field(None, ge=0)

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_teams(self):
        if self.team1_id is not None and self.team2_id is not None:
            if self.team1_id == self.team2_id:
                raise ValueError("team1_id and team2_id must be different")
        return self


class MatchRead(MatchBase):
    id: int
