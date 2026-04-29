from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


# bcrypt is the industry standard password hashing algorithm
# It's intentionally slow — makes brute force attacks very hard
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Convert plain text password to a secure hash.

    Example:
        "secret123"  →  "$2b$12$KIX..."

    The hash is one-way — you cannot reverse it back to "secret123"
    This means even if your database is stolen,
    attackers cannot read your users passwords
    """
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """
    Check if a plain password matches a stored hash.

    Example:
        verify_password("secret123", "$2b$12$KIX...") → True
        verify_password("wrongpass", "$2b$12$KIX...") → False
    """
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict) -> str:
    """
    Create a short-lived JWT access token.

    Access token:
    - Lives for 30 minutes
    - Sent with every API request
    - Used to identify who is making the request
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    # Add expiry time and token type to the payload
    to_encode.update({"exp": expire, "type": "access"})

    # Sign the token with our secret key
    # This makes it impossible to fake
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def create_refresh_token(data: dict) -> str:
    """
    Create a long-lived JWT refresh token.

    Refresh token:
    - Lives for 7 days
    - Only used to get a new access token
    - When access token expires, use this to get a new one
    - User does not need to login again for 7 days
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT token.

    Returns the payload (data inside token) if valid.
    Returns None if token is expired or tampered with.

    Example payload:
        {"sub": "user-uuid-here", "type": "access", "exp": ...}
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        # Token is invalid or expired
        return None