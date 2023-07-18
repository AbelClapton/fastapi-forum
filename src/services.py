from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"

    db_user = models.User(
        email=user.email,
        hashed_password=fake_hashed_password,
        username=user.username,
        balance=user.balance,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_pools(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.Pool).offset(skip).limit(limit).all()


def get_pool(db: Session, pool_id: int):
    return db.query(models.Pool).filter(models.Pool.id == pool_id).first()


def create_pool(db: Session, pool: schemas.PoolCreate):
    db_pool = models.Pool(**pool.dict())
    db.add(db_pool)
    db.commit()
    db.refresh(db_pool)
    return db_pool


def join_user_to_pool(db: Session, pool_id: int, user_id: int):
    pool = get_pool(db, pool_id)
    if not pool:
        raise HTTPException(status_code=404, detail="Pool Not Found")

    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    if user.balance < pool.entry:  # type: ignore
        raise HTTPException(
            status_code=400, detail="Pool's entry is above the user current balance"
        )

    if user in pool.users:
        return

    pool.users.append(user)
    db.commit()


def remove_user_from_pool(db: Session, pool_id: int, user_id: int):
    pool = get_pool(db, pool_id)
    if not pool:
        raise HTTPException(status_code=404, detail="Pool Not Found")

    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    pool.users.remove(user)
    db.commit()
