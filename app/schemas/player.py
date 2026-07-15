"""DTOs (Pydantic schemas) for Player entity."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class PlayerBase(BaseModel):
    nickname: str = Field(..., max_length=100)
    real_name: str = Field(..., max_length=255)
    country: str = Field(..., max_length=100)
    age: int
    role: str = Field(..., max_length=100)
    team_id: int

    model_config = ConfigDict(from_attributes=True)

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(BaseModel):
    nickname: Optional[str] = None
    real_name: Optional[str] = None
    country: Optional[str] = None
    age: Optional[int] = None
    role: Optional[str] = None
    team_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class PlayerRead(PlayerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
