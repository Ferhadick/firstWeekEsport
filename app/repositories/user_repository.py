from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.user import User


def create_user(db: Session, user_data: dict) -> User:
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_by_username_or_email(db: Session, identifier: str) -> User | None:
    return (
        db.query(User)
        .filter((User.username == identifier) | (User.email == identifier))
        .first()
    )


def update_role(db: Session, user_id: int, role: str) -> User | None:
    user = get_by_id(db, user_id)
    if user:
        user.role = role
        db.commit()
        db.refresh(user)
    return user
