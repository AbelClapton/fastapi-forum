from typing import Annotated
from fastapi import Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from ..dependencies import get_session

from .repository import UserRepo
from .models import UserModel
from .schemas import UserCreate, UserUpdate
from .exceptions import UserNotFoundException, UserEmailAlreadyExistsException

DBSession = Annotated[Session, Depends(get_session)]


def get_validated_user(user_id: UUID4, session: DBSession) -> UserModel:
    user = UserRepo.get_user(user_id, session)
    if not user:
        raise UserNotFoundException()
    return user


def get_email_validated_user(
    user: UserCreate | UserUpdate, session: DBSession
) -> UserCreate | UserUpdate:
    db_user = UserRepo.get_user_by_email(user.email, session)
    if db_user:
        raise UserEmailAlreadyExistsException()
    return user


ValidUser = Annotated[UserModel, Depends(get_validated_user)]
ValidUserCreate = Annotated[UserCreate, Depends(get_email_validated_user)]
ValidUserUpdate = Annotated[UserUpdate, Depends(get_email_validated_user)]
