from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TeamBase(BaseModel):
    name: str = Field(
        ...,
        description="The official team name",
        examples=["Fnatic"],
    )
    tag: str = Field(
        ...,
        min_length=2,
        max_length=5,
        description="The team's short tag (2-5 uppercase characters)",
        examples=["FNC"],
    )
    country: str = Field(
        ...,
        description="The country the team is based in",
        examples=["UK"],
    )
    founded_year: int = Field(
        ...,
        gt=1990,
        description="The year the team was founded (must be after 1990)",
        examples=[2004],
    )
    logo_url: Optional[str] = Field(
        None,
        description="URL to the team's logo image",
        examples=["https://example.com/logos/fnc.png"],
    )

    model_config = ConfigDict(from_attributes=True)

    @field_validator("tag")
    @classmethod
    def uppercase_tag(cls, v: str) -> str:
        if not v.isupper():
            raise ValueError("tag must be uppercase")
        return v


class TeamCreate(TeamBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Fnatic",
                "tag": "FNC",
                "country": "UK",
                "founded_year": 2004,
                "logo_url": "https://example.com/logos/fnc.png",
            }
        },
    )


class TeamUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        description="The official team name",
        examples=["G2 Esports"],
    )
    tag: Optional[str] = Field(
        None,
        min_length=2,
        max_length=5,
        description="The team's short tag (2-5 uppercase characters)",
        examples=["G2"],
    )
    country: Optional[str] = Field(
        None,
        description="The country the team is based in",
        examples=["Germany"],
    )
    founded_year: Optional[int] = Field(
        None,
        gt=1990,
        description="The year the team was founded (must be after 1990)",
        examples=[2013],
    )
    logo_url: Optional[str] = Field(
        None,
        description="URL to the team's logo image",
        examples=["https://example.com/logos/g2.png"],
    )

    model_config = ConfigDict(from_attributes=True)

    @field_validator("tag")
    @classmethod
    def uppercase_tag(cls, v: str | None) -> str | None:
        if v is not None and not v.isupper():
            raise ValueError("tag must be uppercase")
        return v


class TeamRead(TeamBase):
    id: int = Field(
        ...,
        description="The unique identifier for the team",
        examples=[1],
    )
