from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserRead
from app.services import auth_service

router = APIRouter(tags=["auth"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a user account with username, email, and password.",
)
def register_endpoint(
    request: RegisterRequest,
    db: Session = Depends(get_db),
) -> UserRead:
    return auth_service.register(db, request)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Log in and get an access token",
    description="Authenticate with username or email and password to receive a JWT.",
)
def login_endpoint(
    request: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    return auth_service.login(db, request)
