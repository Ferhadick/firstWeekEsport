from __future__ import annotations

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.dependencies.database import get_db
from app.exceptions import AuthenticationException, AuthorizationException
from app.models.user import User, UserRole
from app.repositories import user_repository


def get_token_from_header(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise AuthenticationException("Invalid authorization header")
    return authorization.removeprefix("Bearer ")


def get_current_user(
    token: str = Depends(get_token_from_header),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise AuthenticationException("Invalid token payload")

    user = user_repository.get_by_id(db, int(user_id))
    if not user:
        raise AuthenticationException("User not found")

    return user


def require_role(allowed_roles: list[UserRole]):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise AuthorizationException("Insufficient permissions")
        return current_user
    return role_checker
