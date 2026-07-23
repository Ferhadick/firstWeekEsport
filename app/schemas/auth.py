from __future__ import annotations

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=8)


class LoginRequest(BaseModel):
    username: str = Field(..., description="Username or email address")
    password: str = Field(...)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
