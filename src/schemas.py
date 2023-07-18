from __future__ import annotations
from typing import Annotated

from pydantic import BaseModel, Field, EmailStr


class PoolBase(BaseModel):
    entry: Annotated[float, Field(min=1)] = 1
    capacity: Annotated[int, Field(min=2)] = 100


class PoolCreate(PoolBase):
    pass


class Pool(PoolBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    username: Annotated[str | None, Field(min_length=3)] = None
    balance: Annotated[float, Field(min=0)] = 0


class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=3)]


class User(UserBase):
    id: int
    is_active: bool = True
    pools: list[Pool] = []

    class Config:
        orm_mode = True
