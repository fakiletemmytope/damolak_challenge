from uuid import uuid4

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.dependencies import (
    REFRESH_TOKEN_EXPIRE_DAYS,
    TokenType,
    blacklist_token,
    get_current_user,
    get_token,
    hash_password,
    verify_password,
    verify_token,
)
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, UserCreate, UserRead

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserRead, status_code=201)
async def register(
    data: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    result = await session.exec(select(User).where(User.email == data.email))
    user = result.first()
    if user:
        raise HTTPException(status_code=400, detail="Email already exists")
    user_data = data.model_dump(exclude={"password"})
    passwd_hash = hash_password(data.password)
    user = User(**user_data, password=passwd_hash)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.post("/login", response_model=LoginResponse, status_code=200)
async def login(
    data: LoginRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    result = await session.exec(select(User).where(User.email == data.email))
    user = result.first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = get_token(
        payload={
            "id": user.id,
            "jti": str(uuid4()),
        },
        token_type=TokenType.ACCESS,
    )
    refresh_token = get_token(
        payload={
            "id": user.id,
            "jti": str(uuid4()),
        },
        token_type=TokenType.REFRESH,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
    )
    return LoginResponse(user_details=UserRead(**user.model_dump()), token=access_token)


@router.post("/logout", dependencies=[Depends(blacklist_token)])
async def logout(refresh_token: str = Cookie(None)):
    try:
        await blacklist_token(refresh_token)
        print(refresh_token)
        return {"message": "Logout"}
    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=400,
        ) from e


@router.post("/refresh")
async def refresh_access_token(response: Response, refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(status_code=404, detail="no refresh token")
    payload = (await verify_token(refresh_token)).copy()
    await blacklist_token(refresh_token)
    access_token = get_token(
        payload={
            "id": payload["id"],
            "jti": str(uuid4()),
        },
        token_type=TokenType.ACCESS,
    )
    refresh_token = get_token(
        payload={
            "id": payload["id"],
            "jti": str(uuid4()),
        },
        token_type=TokenType.REFRESH,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
    )

    return {"access_token": access_token}


@router.get("/me")
async def get_me(
    session: AsyncSession = Depends(get_session),
    user: UserRead = Depends(get_current_user),
) -> UserRead:
    return user
