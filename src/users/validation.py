from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from ..dependencies import get_session

from .repository import UserRepo
from .models import UserModel
from .schemas import UserCreate, UserUpdate
from .exceptions import UserNotFoundException, UserEmailAlreadyExistsException

DBSession = Annotated[Session, Depends(get_session)]


def get_validated_user(user_id: int, session: DBSession):
    user = UserRepo.get_user(user_id, session)
    if not user:
        raise UserNotFoundException()
    return user


def get_email_validated_user(user: UserCreate | UserUpdate, session: DBSession):
    db_user = UserRepo.get_user_by_email(user.email, session)
    if db_user:
        raise UserEmailAlreadyExistsException()
    return user


ValidatedUser = Annotated[UserModel, Depends(get_validated_user)]
ValidatedUserCreate = Annotated[UserCreate, Depends(get_email_validated_user)]
ValidatedUserUpdate = Annotated[UserUpdate, Depends(get_email_validated_user)]
