"""User repository handling database operations for User entity."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.user import User


def create_user(db: Session, user_data: dict) -> User:
    """Create and persist a new user.

    Args:
        db: The database session.
        user_data: Dictionary of user fields (including password_hash).

    Returns:
        The newly created User ORM instance.

    """
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_by_email(db: Session, email: str) -> User | None:
    """Retrieve a user by email address.

    Args:
        db: The database session.
        email: The email to search for.

    Returns:
        The matching User or None.

    """
    return db.query(User).filter(User.email == email).first()


def get_by_username(db: Session, username: str) -> User | None:
    """Retrieve a user by username.

    Args:
        db: The database session.
        username: The username to search for.

    Returns:
        The matching User or None.

    """
    return db.query(User).filter(User.username == username).first()


def get_by_id(db: Session, user_id: int) -> User | None:
    """Retrieve a user by primary key.

    Args:
        db: The database session.
        user_id: The user ID to search for.

    Returns:
        The matching User or None.

    """
    return db.query(User).filter(User.id == user_id).first()
