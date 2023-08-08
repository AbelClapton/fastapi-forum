from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4

from ..posts.schemas import PostResponse


class UserBase(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    is_active: bool


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDB(UserBase):
    id: UUID4
    hashed_password: str


class UserResponse(UserBase):
    id: int
    posts: list[PostResponse]

    class Config:
        orm_mode = True
