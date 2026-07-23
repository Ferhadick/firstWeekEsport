from __future__ import annotations

import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

_EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


class UserBase(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="The user's unique display name (3-50 characters)",
        examples=["newuser"],
    )
    email: str = Field(
        ...,
        description="The user's email address",
        examples=["user@example.com"],
    )

    model_config = ConfigDict(from_attributes=True)

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        if not _EMAIL_PATTERN.match(v):
            raise ValueError("Invalid email format")
        return v.lower()


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        description="The user's password (minimum 8 characters)",
        examples=["securePass123"],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "username": "newuser",
                "email": "user@example.com",
                "password": "securePass123",
            }
        },
    )


class UserLogin(BaseModel):
    email: str = Field(
        ...,
        description="The user's email address",
        examples=["user@example.com"],
    )
    password: str = Field(
        ...,
        description="The user's password",
        examples=["securePass123"],
    )


class UserRead(UserBase):
    id: int = Field(
        ...,
        description="The unique identifier for the user",
        examples=[1],
    )
    role: str = Field(
        ...,
        description="The user's role (USER or ADMIN)",
        examples=["USER"],
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the user account was created",
        examples=[datetime(2026, 1, 15, 10, 30, 0)],
    )
