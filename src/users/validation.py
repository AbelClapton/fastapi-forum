from typing import Annotated
from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session

from ..dependencies import get_session

from .repository import UserRepo
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
