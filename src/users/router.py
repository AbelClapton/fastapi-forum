from fastapi import APIRouter, status

from ..schemas import Message
from ..dependencies import DBSession
from ..auth.dependencies import CurrentUser

from .schemas import UserResponse
from .services import UserService
from .dependencies import ValidUser, ValidUserCreate, ValidUserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_users(session: DBSession, skip: int = 0, limit: int = 10):
    return UserService.get_users(skip, limit, session)


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_current_user(user: CurrentUser):
    return user


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user: ValidUser):
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: ValidUserCreate,
    session: DBSession,
):
    return UserService.create_user(user, session)


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(
    user: ValidUser,
    update_data: ValidUserUpdate,
    session: DBSession,
):
    return UserService.update_user(user, update_data, session)


@router.delete("/{user_id}", response_model=Message, status_code=status.HTTP_200_OK)
def delete_user(user: ValidUser, session: DBSession):
    UserService.delete_user(user, session)
    return Message(message="User deleted succefully")
