from fastapi import Depends
from sqlalchemy.orm import Session

from ..hasher import hash

from .models import UserModel
from .schemas import UserCreate, UserUpdate


class UserRepo:
    @staticmethod
    def get_users(skip: int, limit: int, session: Session):
        return session.query(UserModel).offset(skip).limit(limit).all()

    @staticmethod
    def get_user(user_id: int, session: Session) -> UserModel | None:
        return session.query(UserModel).filter(UserModel.id == user_id).first()

    @staticmethod
    def get_user_by_email(email: str, session: Session):
        return session.query(UserModel).filter(UserModel.email == email).first()

    @staticmethod
    def create_user(user: UserCreate, session: Session):
        db_user = UserModel(
            name=user.name, email=user.email, hashed_password=user.password
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

    @staticmethod
    def update_user(
        user: UserModel, update_data: UserUpdate, session: Session
    ) -> UserModel:
        if update_data.name:
            user.name = update_data.name
        if update_data.email:
            user.email = update_data.email
        if update_data.password:
            user.hashed_password = hash(update_data.password)

        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def delete_user(user: UserModel, session: Session):
        session.delete(user)
        session.commit()
