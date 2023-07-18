from __future__ import annotations

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .database import Base

user_pool = Table(
    "user_pool",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("pool_id", Integer, ForeignKey("pools.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    # TODO: Use UUID
    id = mapped_column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, default=None)
    balance = Column(Float, default=0)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    pools: Mapped[list[Pool]] = relationship(
        secondary=user_pool, back_populates="users"
    )


class Pool(Base):
    __tablename__ = "pools"

    id = mapped_column(Integer, primary_key=True, index=True)
    entry = Column(Float, index=True)
    capacity = Column(Integer, index=True)

    users: Mapped[list[User]] = relationship(
        secondary=user_pool, back_populates="pools"
    )
