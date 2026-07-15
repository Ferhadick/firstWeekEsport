"""Data Transfer Objects (DTO) for Team model."""

from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class TeamBase(BaseModel):
    name: str = Field(..., max_length=255)
    tag: str = Field(..., max_length=16)
    country: str = Field(..., max_length=100)
    founded_year: int
    logo_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class TeamCreate(TeamBase):
    pass

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    tag: Optional[str] = None
    country: Optional[str] = None
    founded_year: Optional[int] = None
    logo_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class TeamRead(TeamBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
