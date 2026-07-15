"""DTOs (Pydantic schemas) for Match entity."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


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
    score_team1: Optional[int] = None
    score_team2: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class MatchCreate(MatchBase):
    pass


class MatchUpdate(BaseModel):
    tournament_id: Optional[int] = None
    team1_id: Optional[int] = None
    team2_id: Optional[int] = None
    scheduled_at: Optional[datetime] = None
    status: Optional[MatchStatus] = None
    winner_id: Optional[int] = None
    score_team1: Optional[int] = None
    score_team2: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class MatchRead(MatchBase):
    id: int
