from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import jwt


from ..users.repository import UserRepo
from ..hasher import verify_hash
from ..config import settings

from .exceptions import InvalidCredentialsException


class AuthService:
    @staticmethod
    def authenticate_user(email: str, password: str, session: Session):
        user = UserRepo.get_user_by_email(email, session)
        if not user or not verify_hash(password, user.hashed_password):
            raise InvalidCredentialsException()
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt
