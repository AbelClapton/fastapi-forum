from fastapi import APIRouter, status

from ..dependencies import DBSession
from ..schemas import Message
from ..auth.dependencies import CurrentUser
from ..exceptions import UnauthorizedException

from .services import PostService
from .schemas import PostResponse, PostCreate, PostUpdate
from .dependencies import ValidPost, ValidOwnedPost

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[PostResponse], status_code=status.HTTP_200_OK)
def get_posts(session: DBSession):
    return PostService.get_posts(session)


@router.get("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
def get_post(post: ValidPost):
    return post


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, current_user: CurrentUser, session: DBSession):
    return PostService.create_post(post, current_user.id, session)


@router.put("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
def update_post(
    post: ValidOwnedPost,
    update_data: PostUpdate,
    session: DBSession,
):
    return PostService.update_post(post, update_data, session)


@router.delete("/{post_id}", response_model=Message, status_code=status.HTTP_200_OK)
def delete_post(post: ValidOwnedPost, session: DBSession):
    PostService.delete_post(post, session)
    return Message(message="Post deleted successfully")
