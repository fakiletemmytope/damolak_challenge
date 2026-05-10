from datetime import datetime

from pydantic import BaseModel

from app.models.user import Role


class UserCreate(BaseModel):
    email: str
    password: str
    role: Role | None = None

class UserRead(BaseModel):
    id: int
    email: str
    role: Role
    is_active: bool
    date_created: datetime
    date_updated: datetime = None

class UserUpdate(BaseModel):
    is_active: bool = None
    
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    token: str
    refresh_token: str | None = None
    user_details: UserRead
