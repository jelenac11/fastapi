from uuid import UUID

from pydantic import BaseModel

from api.schemas.base import SafeBaseModel


class TagBaseResponse(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True


class CommentBaseResponse(BaseModel):
    id: UUID
    content: str
    user_id: UUID
    post_id: UUID

    class Config:
        from_attributes = True


class UserBaseResponse(BaseModel):
    id: UUID
    username: str

    class Config:
        from_attributes = True


class PostBaseResponse(BaseModel):
    id: UUID
    title: str
    content: str
    status: str

    class Config:
        from_attributes = True


class UserResponse(UserBaseResponse, SafeBaseModel):
    comments: list[CommentBaseResponse] | None = None
    posts: list[PostBaseResponse] | None = None


class PostResponse(PostBaseResponse, SafeBaseModel):
    user: UserBaseResponse | None
    comments: list[CommentBaseResponse]
    tags: list[TagBaseResponse]
