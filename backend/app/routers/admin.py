from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.dependencies import get_current_user, user_role
from app.models.user import Role, User
from app.schemas.auth import UserRead

router = APIRouter(prefix="/admin")


@router.get("/users")
async def get_users(
    session: AsyncSession = Depends(get_session),
    user: UserRead = Depends(get_current_user),     
    user_role: Role = Depends(user_role),
) -> list[UserRead]:
    if user_role != Role.ADMIN:
        raise HTTPException(detail="unauthorized", status_code=401)
    result = await session.exec(select(User))
    users = result.all()
    return users
