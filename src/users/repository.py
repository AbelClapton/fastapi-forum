from fastapi import Depends
from sqlalchemy.orm import Session

from ..hasher import get_password_hash

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
    def update_user(user_id: int, user: UserUpdate, session: Session):
        db_user: UserModel = UserRepo.get_user(user_id, session)
        if not db_user:
            return

        if user.name:
            db_user.name = user.name
        if user.email:
            db_user.email = user.email
        if user.password:
            db_user.hashed_password = get_password_hash(user.password)

        session.commit()
        session.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(user: UserModel, session: Session):
        session.delete(user)
        session.commit()
