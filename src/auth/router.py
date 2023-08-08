from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas import Message
from ..dependencies import DBSession

from .dependencies import FormData, AuthToken
from .services import AuthService
from .schemas import Token

router = APIRouter(tags=["Auth"])


@router.get("/test", response_model=Message, status_code=status.HTTP_200_OK)
def get_health(token: AuthToken):
    return {"message": token}


@router.post("/token", response_model=Token)
async def login(form_data: FormData, session: DBSession):
    user = AuthService.authenticate_user(
        form_data.username, form_data.password, session
    )
    access_token = AuthService.create_access_token(data={"sub": f"{user.id}"})
    return {"access_token": access_token, "token_type": "bearer"}
