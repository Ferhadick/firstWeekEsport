"""DTOs (Pydantic schemas) for User entity."""

from __future__ import annotations

import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

_EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


class UserBase(BaseModel):
    """Shared fields between create and read schemas."""

    username: str = Field(..., min_length=3, max_length=50)
    email: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        """Validate email format and normalize to lowercase."""
        if not _EMAIL_PATTERN.match(v):
            raise ValueError("Invalid email format")
        return v.lower()


class UserCreate(UserBase):
    """Schema for user registration (includes plain-text password)."""

    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    """Schema for user login request."""

    email: str
    password: str


class UserRead(UserBase):
    """Schema for user responses (never exposes password_hash)."""

    id: int
    role: str
    created_at: datetime
