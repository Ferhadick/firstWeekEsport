"""Data Transfer Objects (DTO) for Team model."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TeamBase(BaseModel):
    name: str = Field(...)
    tag: str = Field(..., min_length=2, max_length=5)
    country: str = Field(...)
    founded_year: int = Field(..., gt=1990)
    logo_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("tag")
    @classmethod
    def uppercase_tag(cls, v: str) -> str:
        if not v.isupper():
            raise ValueError("tag must be uppercase")
        return v


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    tag: Optional[str] = Field(None, min_length=2, max_length=5)
    country: Optional[str] = None
    founded_year: Optional[int] = Field(None, gt=1990)
    logo_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("tag")
    @classmethod
    def uppercase_tag(cls, v: str | None) -> str | None:
        if v is not None and not v.isupper():
            raise ValueError("tag must be uppercase")
        return v


class TeamRead(TeamBase):
    id: int
