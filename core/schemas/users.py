from datetime import datetime
from pydantic import BaseModel, EmailStr
from .base import BaseSchema

class UserBase(BaseSchema):
    username: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseSchema):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: str | None = None

class UserResponse(UserBase):
    id: int
    created_at: datetime 