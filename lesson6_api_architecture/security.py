"""Password checking, token verification, and reusable permission checks."""

import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Literal

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel, ConfigDict, Field, SecretStr
from pwdlib import PasswordHash


SECRET_KEY = os.environ.get("JWT_SECRET", "")
if len(SECRET_KEY.encode("utf-8")) < 32:
    raise RuntimeError("Set JWT_SECRET to a randomly generated secret of at least 32 bytes.")

ALGORITHM = "HS256"
TOKEN_MINUTES = 15
ISSUER = "warranty-lesson"
AUDIENCE = "warranty-api"
password_hasher = PasswordHash.recommended()
bearer_scheme = HTTPBearer(auto_error=False)


class User(BaseModel):
    username: str
    role: Literal["homeowner", "technician"]
    property_ids: set[int]


class StoredUser(User):
    password_hash: str
    disabled: bool = False


class LoginInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username: str = Field(min_length=1, max_length=80)
    password: SecretStr = Field(min_length=1, max_length=256)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = TOKEN_MINUTES * 60


# All three PUBLIC DEMO accounts use LearnOnly-123! (never use it for real users).
# The store contains an Argon2 hash, not a plaintext password.
DEMO_HASH = "$argon2id$v=19$m=65536,t=3,p=4$yd/2vtEhwf2uz6SXHX8DBg$+PYJxgkF6g/MY+OtaTE3Zu+6s6RX12QcSNPO47LDYFk"
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$GpcoLEWApXkN/l3T+3GhCw$yJEYXc4En+JajrU8hTRgpY5B1hclECZPtjnq9r2QZds"

USERS = {
    "owner3": StoredUser(username="owner3", role="homeowner", property_ids={3}, password_hash=DEMO_HASH),
    "owner4": StoredUser(username="owner4", role="homeowner", property_ids={4}, password_hash=DEMO_HASH),
    "steven": StoredUser(username="steven", role="technician", property_ids={3}, password_hash=DEMO_HASH),
}


def authentication_error() -> HTTPException:
    return HTTPException(
        status_code=401,
        detail="Invalid or missing credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def authenticate_user(username: str, password: str) -> StoredUser:
    user = USERS.get(username)
    # Even an unknown username performs a password-hash check.
    stored_hash = user.password_hash if user else DUMMY_HASH
    password_is_valid = password_hasher.verify(password, stored_hash)
    if user is None or not password_is_valid or user.disabled:
        raise authentication_error()
    return user


def create_access_token(username: str) -> str:
    now = datetime.now(timezone.utc)
    claims = {
        "sub": username,
        "iat": now,
        "exp": now + timedelta(minutes=TOKEN_MINUTES),
        "iss": ISSUER,
        "aud": AUDIENCE,
    }
    return jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> User:
    if credentials is None:
        raise authentication_error()

    try:
        claims = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            issuer=ISSUER,
            audience=AUDIENCE,
            options={"require": ["sub", "iat", "exp", "iss", "aud"]},
        )
    except InvalidTokenError:
        raise authentication_error() from None

    username = claims.get("sub")
    if not isinstance(username, str):
        raise authentication_error()
    user = USERS.get(username)
    if user is None or user.disabled:
        raise authentication_error()

    # Load CURRENT permissions from the server; don't trust a client-supplied role.
    # Return a public object without the stored password hash.
    return User(username=user.username, role=user.role, property_ids=user.property_ids)


def require_technician(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    if user.role != "technician":
        raise HTTPException(status_code=403, detail="Technician role required")
    return user


def check_property_access(user: User, property_id: int) -> None:
    if property_id not in user.property_ids:
        raise HTTPException(status_code=403, detail="No access to this property")
