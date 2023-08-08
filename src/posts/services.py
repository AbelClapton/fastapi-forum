from sqlalchemy.orm import Session

from .repository import PostRepo
from .models import PostModel
from .schemas import PostCreate, PostUpdate


class PostService:
    @staticmethod
    def get_posts(session: Session) -> list[PostModel]:
        return PostRepo.get_posts(session)

    @staticmethod
    def get_post(post_id: int, session: Session) -> PostModel | None:
        return PostRepo.get_post(post_id, session)

    @staticmethod
    def create_post(post: PostCreate, user_id: int, session: Session):
        return PostRepo.create_post(post, user_id, session)

    @staticmethod
    def update_post(post: PostModel, update_data: PostUpdate, session: Session):
        return PostRepo.update_post(post, update_data, session)

    @staticmethod
    def delete_post(post: PostModel, session: Session):
        return PostRepo.delete_post(post, session)
