from sqlalchemy.orm import Session

from ..hasher import hash

from .models import UserModel
from .schemas import UserCreate, UserUpdate
from .repository import UserRepo


class UserService:
    @staticmethod
    def get_users(skip: int, limit: int, session: Session):
        return UserRepo.get_users(skip, limit, session)

    @staticmethod
    def get_user(user_id: int, session: Session):
        return UserRepo.get_user(user_id, session)

    @staticmethod
    def create_user(user: UserCreate, session: Session):
        print(user.password)
        user.password = hash(user.password)
        return UserRepo.create_user(user, session)

    @staticmethod
    def update_user(user: UserModel, update_data: UserUpdate, session: Session):
        return UserRepo.update_user(user, update_data, session)

    @staticmethod
    def delete_user(user: UserModel, session: Session):
        return UserRepo.delete_user(user, session)
