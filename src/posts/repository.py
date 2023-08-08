from sqlalchemy.orm import Session

from .models import PostModel
from .schemas import PostCreate, PostUpdate


class PostRepo:
    @staticmethod
    def get_posts(session: Session) -> list[PostModel]:
        return session.query(PostModel).all()

    @staticmethod
    def get_post(post_id: int, session: Session) -> PostModel | None:
        return session.query(PostModel).filter(PostModel.id == post_id).first()

    @staticmethod
    def create_post(post: PostCreate, user_id: int, session: Session) -> PostModel:
        db_post = PostModel(**post.dict(), owner_id=user_id)
        session.add(db_post)
        session.commit()
        session.refresh(db_post)
        return db_post

    @staticmethod
    def update_post(
        post: PostModel, update_data: PostUpdate, session: Session
    ) -> PostModel:
        if update_data.title:
            post.title = update_data.title
        if update_data.content:
            post.content = update_data.content
        session.commit()
        session.refresh(post)
        return post

    @staticmethod
    def delete_post(post: PostModel, session: Session):
        session.delete(post)
        session.commit()
