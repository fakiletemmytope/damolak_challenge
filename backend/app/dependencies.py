from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import ALGORITHM, SECRET_KEY
from app.database import get_session
from app.models.user import User
from app.redis_client import r
from app.schemas.auth import UserRead

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


class TokenType(Enum):
    REFRESH = "refresh"
    ACCESS = "access"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_token(
    payload: dict[str, Any],
    token_type: TokenType = TokenType.ACCESS,
) -> str:
    to_encode = payload.copy()
    if token_type == TokenType.ACCESS:
        to_encode["exp"] = datetime.now(tz=UTC) + timedelta(minutes=30)
        to_encode["type"] = "access"
    else:
        to_encode["exp"] = datetime.now(tz=UTC) + timedelta(days=7)
        to_encode["type"] = "refresh"

    token = jwt.encode(
        payload=to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return token


async def verify_token(token: str):
    try:
        decoded = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=ALGORITHM)
        jti = decoded["jti"]
        if await r.exists(f"blacklist_{jti}"):
            raise HTTPException(detail="Token expired", status_code=400)
        return decoded
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(detail="Token expired", status_code=400) from e
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400) from e



async def blacklist_token(token: str = Depends(oauth2_scheme)):
    decoded = await verify_token(token)
    jti = decoded["jti"]
    exp = decoded["exp"]
    now = datetime.now(tz=UTC).timestamp()
    ttl = int(exp - now)
    await r.setex(name=f"blacklist_{jti}", time=max(ttl, 0), value="blacklisted")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    payload = await verify_token(token)
    result = await session.exec(select(User).where(User.id == payload["id"]))
    user = result.first()
    if not user:
        raise HTTPException(detail="user not found", status_code=404)
    return user


async def user_role(user: UserRead = Depends(get_current_user)) -> str:
    if user.role is None:
        raise HTTPException(detail="user role not set", status_code=400)
    return user.role.value
