from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PlayerBase(BaseModel):
    nickname: str = Field(
        ...,
        description="The player's in-game nickname",
        examples=["Caps"],
    )
    real_name: str = Field(
        ...,
        description="The player's real full name",
        examples=["Rasmus Winther"],
    )
    country: str = Field(
        ...,
        max_length=100,
        description="The player's country of origin",
        examples=["Denmark"],
    )
    age: int = Field(
        ...,
        ge=13,
        le=60,
        description="The player's age (must be between 13 and 60)",
        examples=[25],
    )
    role: str = Field(
        ...,
        description="The player's role or position",
        examples=["Mid Laner"],
    )
    team_id: int = Field(
        ...,
        gt=0,
        description="The ID of the team the player belongs to",
        examples=[1],
    )

    model_config = ConfigDict(from_attributes=True)


class PlayerCreate(PlayerBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "nickname": "Caps",
                "real_name": "Rasmus Winther",
                "country": "Denmark",
                "age": 25,
                "role": "Mid Laner",
                "team_id": 1,
            }
        },
    )


class PlayerUpdate(BaseModel):
    nickname: Optional[str] = Field(
        None,
        description="The player's in-game nickname",
        examples=["Rekkles"],
    )
    real_name: Optional[str] = Field(
        None,
        description="The player's real full name",
        examples=["Martin Larsson"],
    )
    country: Optional[str] = Field(
        None,
        max_length=100,
        description="The player's country of origin",
        examples=["Sweden"],
    )
    age: Optional[int] = Field(
        None,
        ge=13,
        le=60,
        description="The player's age (must be between 13 and 60)",
        examples=[24],
    )
    role: Optional[str] = Field(
        None,
        description="The player's role or position",
        examples=["Bot Laner"],
    )
    team_id: Optional[int] = Field(
        None,
        gt=0,
        description="The ID of the team the player belongs to",
        examples=[2],
    )

    model_config = ConfigDict(from_attributes=True)


class PlayerRead(PlayerBase):
    id: int = Field(
        ...,
        description="The unique identifier for the player",
        examples=[1],
    )
