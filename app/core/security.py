from __future__ import annotations

from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.core.config import (
    get_access_token_expire_minutes,
    get_jwt_algorithm,
    get_jwt_secret,
)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=get_access_token_expire_minutes(),
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, get_jwt_secret(), algorithm=get_jwt_algorithm())


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token,
            get_jwt_secret(),
            algorithms=[get_jwt_algorithm()],
        )
    except JWTError:
        return None
