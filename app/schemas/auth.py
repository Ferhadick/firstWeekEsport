from __future__ import annotations

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="The user's unique display name (3-50 characters)",
        examples=["pro_player"],
    )
    email: str = Field(
        ...,
        max_length=255,
        description="The user's email address",
        examples=["player@example.com"],
    )
    password: str = Field(
        ...,
        min_length=8,
        description="The user's password (minimum 8 characters)",
        examples=["securePassword123"],
    )


class LoginRequest(BaseModel):
    username: str = Field(
        ...,
        description="Username or email address for authentication",
        examples=["pro_player"],
    )
    password: str = Field(
        ...,
        description="The user's password",
        examples=["securePassword123"],
    )


class TokenResponse(BaseModel):
    access_token: str = Field(
        ...,
        description="JWT access token for authenticating subsequent requests",
        examples=["eyJhbGciOiJIUzI1NiIs..."],
    )
    token_type: str = Field(
        "bearer",
        description="Type of the token (always 'bearer')",
        examples=["bearer"],
    )
