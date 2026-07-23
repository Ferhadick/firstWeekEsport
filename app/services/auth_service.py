from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.exceptions import AlreadyExistsException, BusinessValidationException
from app.repositories import user_repository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserRead


def register(db: Session, request: RegisterRequest) -> UserRead:
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

    user = user_repository.create_user(db, user_data)
    return UserRead.model_validate(user)


def login(db: Session, request: LoginRequest) -> TokenResponse:
    user = user_repository.get_by_username_or_email(db, request.username)
    if not user:
        raise BusinessValidationException("Invalid credentials")

    if not verify_password(request.password, user.password_hash):
        raise BusinessValidationException("Invalid credentials")

    token = create_access_token(
        data={
            "sub": str(user.id),
            "username": user.username,
            "role": user.role,
        },
    )
    return TokenResponse(access_token=token)
