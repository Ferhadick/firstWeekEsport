from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.security import create_access_token, decode_access_token, hash_password, verify_password
from app.exceptions import AlreadyExistsException, AuthenticationException, AuthorizationException, BusinessValidationException, NotFoundException
from app.models.user import User, UserRole
from app.repositories import user_repository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserRead


def _build_token(user: User) -> str:
    return create_access_token(
        data={
            "sub": str(user.id),
            "username": user.username,
            "role": user.role,
        },
    )


def register(db: Session, request: RegisterRequest, is_admin: bool = False) -> TokenResponse:
    existing_username = user_repository.get_by_username(db, request.username)
    if existing_username:
        raise AlreadyExistsException(
            f"Username '{request.username}' is already taken",
        )

    existing_email = user_repository.get_by_email(db, request.email)
    if existing_email:
        raise AlreadyExistsException(
            f"Email '{request.email}' is already registered",
        )

    user_data = request.model_dump(exclude={"password"})
    user_data["password_hash"] = hash_password(request.password)
    if is_admin:
        user_data["role"] = UserRole.ADMIN

    user = user_repository.create_user(db, user_data)
    token = _build_token(user)
    return TokenResponse(access_token=token)


def login(db: Session, request: LoginRequest) -> TokenResponse:
    user = user_repository.get_by_username_or_email(db, request.username)
    if not user:
        raise BusinessValidationException("Invalid credentials")

    if not verify_password(request.password, user.password_hash):
        raise BusinessValidationException("Invalid credentials")

    token = _build_token(user)
    return TokenResponse(access_token=token)


def get_current_user_info(user: User) -> UserRead:
    return UserRead.model_validate(user)


def promote_user(db: Session, target_user_id: int, new_role: str) -> UserRead:
    if new_role not in (UserRole.USER, UserRole.ADMIN):
        raise BusinessValidationException(f"Invalid role '{new_role}'. Must be USER or ADMIN.")

    user = user_repository.update_role(db, target_user_id, new_role)
    if not user:
        raise NotFoundException(f"User with id {target_user_id} not found")

    return UserRead.model_validate(user)


def refresh_token(token: str) -> TokenResponse:
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise AuthenticationException("Invalid token payload")

    new_token = create_access_token(
        data={
            "sub": payload["sub"],
            "username": payload.get("username", ""),
            "role": payload.get("role", "USER"),
        },
    )
    return TokenResponse(access_token=new_token)
