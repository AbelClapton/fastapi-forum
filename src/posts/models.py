from sqlalchemy import Integer, String, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base, engine


class PostModel(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    owner_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("users.id"))

    owner = relationship("UserModel", back_populates="posts")


Base.metadata.create_all(bind=engine)
