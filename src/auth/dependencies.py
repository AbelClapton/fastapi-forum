from __future__ import annotations
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError

from ..config import settings
from ..dependencies import DBSession
from ..users.models import UserModel
from ..users.services import UserService
from ..users.exceptions import UserNotFoundException

from .exceptions import InvalidCredentialsException, InactiveUserException


async def get_current_user(token: AuthToken, session: DBSession):
    print(token)
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise InvalidCredentialsException()
    except JWTError:
        raise InvalidCredentialsException()

    user = UserService.get_user(user_id, session)
    if not user:
        raise UserNotFoundException()
    return user


async def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise InactiveUserException()
    return current_user


AuthToken = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]
FormData = Annotated[OAuth2PasswordRequestForm, Depends()]
CurrentUser = Annotated[UserModel, Depends(get_current_user)]
