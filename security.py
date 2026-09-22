from typing import Literal
from uuid import uuid4
from datetime import datetime, timezone, timedelta

from passlib.context import CryptContext
import jwt

from config import settings


password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def create_jwt_token(
    user_id: str,
    token_type: Literal["access", "refresh"],
    expires_delta: timedelta,
) -> str:

    expiry = utc_now() + expires_delta

    payload = {
        "sub": user_id,
        "token": token_type,
        "exp": expiry,
        "iat": utc_now(),
        "jti": str(uuid4()),
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decrypt_jwt_token(token: str) -> dict:

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        return payload

    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")

    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")