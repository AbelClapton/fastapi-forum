from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base, engine


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str]= mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)


Base.metadata.create_all(bind=engine)
