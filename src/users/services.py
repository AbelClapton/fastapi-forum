from pydantic import UUID4
from sqlalchemy.orm import Session

from ..hasher import hash

from .models import UserModel
from .schemas import UserCreate, UserUpdate
from .repository import UserRepo


class UserService:
    @staticmethod
    def get_users(skip: int, limit: int, session: Session) -> list[UserModel]:
        return UserRepo.get_users(skip, limit, session)

    @staticmethod
    def get_user(user_id: UUID4, session: Session) -> UserModel:
        return UserRepo.get_user(user_id, session)

    @staticmethod
    def create_user(user: UserCreate, session: Session) -> UserModel:
        print(user.password)
        user.password = hash(user.password)
        return UserRepo.create_user(user, session)

    @staticmethod
    def update_user(
        user: UserModel, update_data: UserUpdate, session: Session
    ) -> UserModel:
        return UserRepo.update_user(user, update_data, session)

    @staticmethod
    def delete_user(user: UserModel, session: Session) -> None:
        UserRepo.delete_user(user, session)
