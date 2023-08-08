from __future__ import annotations
from typing import Annotated
from fastapi import Depends

from ..users.models import UserModel
from ..dependencies import DBSession
from ..exceptions import UnauthorizedException
from ..users.validation import ValidatedUser

from .models import PostModel
from .exceptions import PostNotFoundException
from .repository import PostRepo


def get_validated_post(post_id: int, session: DBSession) -> PostModel:
    post = PostRepo.get_post(post_id, session)
    if not post:
        raise PostNotFoundException()
    return post


def get_validated_owner_post(post: ValidatedPost, user: ValidatedUser) -> bool:
    if not post.id == user.id:
        raise UnauthorizedException()
    return True


ValidatedPost = Annotated[PostModel, Depends(get_validated_post)]
ValidatedOwnerPost = Annotated[PostModel, Depends(get_validated_owner_post)]
