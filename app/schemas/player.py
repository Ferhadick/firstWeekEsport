

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PlayerBase(BaseModel):
    nickname: str = Field(...)
    real_name: str = Field(...)
    country: str = Field(..., max_length=100)
    age: int = Field(..., ge=13, le=60)
    role: str = Field(...)
    team_id: int

    model_config = ConfigDict(from_attributes=True)


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(BaseModel):
    nickname: Optional[str] = None
    real_name: Optional[str] = None
    country: Optional[str] = None
    age: Optional[int] = Field(None, ge=13, le=60)
    role: Optional[str] = None
    team_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class PlayerRead(PlayerBase):
    id: int
