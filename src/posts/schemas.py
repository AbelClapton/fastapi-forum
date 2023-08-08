from pydantic import BaseModel, UUID4


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class DBPost(PostBase):
    id: int
    owner_id: UUID4


class PostResponse(DBPost):
    pass

    class Config:
        orm_mode = True
