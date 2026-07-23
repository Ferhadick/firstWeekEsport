from __future__ import annotations

from fastapi import APIRouter, Depends, Header, Response, status
from sqlalchemy.orm import Session

from app.core.config import get_access_token_expire_minutes, get_admin_secret
from app.dependencies.auth import get_current_user, get_token, require_role
from app.dependencies.database import get_db
from app.models.user import User, UserRole
from app.schemas.auth import LoginRequest, RegisterRequest, RoleUpdateRequest, TokenResponse
from app.schemas.user import UserRead
from app.services import auth_service

router = APIRouter(tags=["auth"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a user account and receive a JWT. Include X-Admin-Secret header to create an ADMIN.",
)
def register_endpoint(
    request: RegisterRequest,
    response: Response,
    x_admin_secret: str | None = Header(None, alias="X-Admin-Secret"),
    db: Session = Depends(get_db),
) -> TokenResponse:
    is_admin = bool(x_admin_secret) and x_admin_secret == get_admin_secret()
    result = auth_service.register(db, request, is_admin=is_admin)
    expire_minutes = get_access_token_expire_minutes()
    response.set_cookie(
        key="access_token",
        value=result.access_token,
        httponly=True,
        max_age=expire_minutes * 60,
        path="/",
        samesite="lax",
    )
    return result


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Log in and get an access token",
    description="Authenticate with username or email and password to receive a JWT.",
)
def login_endpoint(
    request: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> TokenResponse:
    result = auth_service.login(db, request)
    expire_minutes = get_access_token_expire_minutes()
    response.set_cookie(
        key="access_token",
        value=result.access_token,
        httponly=True,
        max_age=expire_minutes * 60,
        path="/",
        samesite="lax",
    )
    return result


@router.get(
    "/me",
    response_model=UserRead,
    summary="Get current user",
    description="Return the authenticated user's profile.",
)
def me_endpoint(
    current_user: User = Depends(get_current_user),
) -> UserRead:
    return auth_service.get_current_user_info(current_user)


@router.put(
    "/users/{user_id}/role",
    response_model=UserRead,
    summary="Change user role",
    description="ADMIN-only. Promote or demote a user by ID.",
)
def promote_endpoint(
    user_id: int,
    body: RoleUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN])),
) -> UserRead:
    return auth_service.promote_user(db, user_id, body.role)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Issue a new access token from a valid existing one.",
)
def refresh_endpoint(
    response: Response,
    token: str = Depends(get_token),
) -> TokenResponse:
    result = auth_service.refresh_token(token)
    expire_minutes = get_access_token_expire_minutes()
    response.set_cookie(
        key="access_token",
        value=result.access_token,
        httponly=True,
        max_age=expire_minutes * 60,
        path="/",
        samesite="lax",
    )
    return result
