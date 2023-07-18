from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, services

router = APIRouter(prefix="/pools", tags=["pools"])


@router.get("/", response_model=list[schemas.Pool])
def read_pools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pools = services.get_pools(db, skip=skip, limit=limit)
    return pools


@router.get("/{pool_id}", response_model=schemas.Pool)
def read_pool(pool_id: int, db: Session = Depends(get_db)):
    pool = services.get_pool(db, pool_id)
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found")
    return pool


@router.post("/")
def create_pool(pool: schemas.PoolCreate, db: Session = Depends(get_db)):
    return services.create_pool(db, pool)


@router.post("/{pool_id}/join")
def join_pool(
    pool_id: int, user_id: Annotated[int, Body()], db: Session = Depends(get_db)
):
    return services.join_user_to_pool(db, pool_id, user_id)


@router.post("/{pool_id}/leave")
def leave_pool(
    pool_id: int, user_id: Annotated[int, Body()], db: Session = Depends(get_db)
):
    return services.remove_user_from_pool(db, pool_id, user_id)
