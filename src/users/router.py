from typing import Annotated
from fastapi import APIRouter, Depends, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from ..schemas import Message
from ..dependencies import get_session

from .models import UserModel
from .schemas import UserResponse, UserCreate, UserUpdate
from .services import UserService
from .validation import get_validated_user, get_email_validated_user

router = APIRouter(prefix="/users", tags=["Users"])
DBSession = Annotated[Session, Depends(get_session)]
ValidatedUser = Annotated[UserModel, Depends(get_validated_user)]
ValidatedUserCreate = Annotated[UserCreate, Depends(get_email_validated_user)]
ValidatedUserUpdate = Annotated[UserUpdate, Depends(get_email_validated_user)]


@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_users(session: DBSession, skip: int = 0, limit: int = 10):
    return UserService.get_users(skip, limit, session)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user: ValidatedUser):
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: ValidatedUserCreate,
    session: DBSession,
):
    return UserService.create_user(user, session)


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(
    user: ValidatedUser,
    update_data: ValidatedUserUpdate,
    session: DBSession,
):
    return UserService.update_user(user.id, update_data, session)


@router.delete("/{user_id}", response_model=Message, status_code=status.HTTP_200_OK)
def delete_user(user: ValidatedUser, session: DBSession):
    if UserService.delete_user(user, session):
        return Message(message="User deleted succefully")
