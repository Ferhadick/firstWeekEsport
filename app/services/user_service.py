"""User service containing business logic for User entity."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.exceptions import AlreadyExistsException
from app.repositories.user_repository import (
    create_user as repo_create_user,
    get_by_email as repo_get_by_email,
    get_by_username as repo_get_by_username,
)
from app.schemas.user import UserCreate, UserRead


def create_user(db: Session, user_in: UserCreate) -> UserRead:
    """Register a new user.

    Validates uniqueness of username and email, hashes the password,
    persists the user, and returns a safe representation.

    Args:
        db: The database session.
        user_in: The validated user creation data.

    Returns:
        A UserRead DTO (password_hash never exposed).

    Raises:
        AlreadyExistsException: If the username or email is taken.

    """
    existing_username = repo_get_by_username(db, user_in.username)
    if existing_username:
        raise AlreadyExistsException(
            f"Username '{user_in.username}' is already taken",
        )

    existing_email = repo_get_by_email(db, user_in.email)
    if existing_email:
        raise AlreadyExistsException(
            f"Email '{user_in.email}' is already registered",
        )

    user_data = user_in.model_dump(exclude={"password"})
    user_data["password_hash"] = hash_password(user_in.password)

    user = repo_create_user(db, user_data)
    return UserRead.model_validate(user)
