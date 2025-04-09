from uuid import UUID

from pydantic import BaseModel, ConfigDict

from api.schemas.base import SafeBaseModel


class BaseResponse(BaseModel):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class TagBaseResponse(BaseResponse):
    name: str


class CommentBaseResponse(BaseResponse):
    content: str
    user_id: UUID
    post_id: UUID


class UserBaseResponse(BaseResponse):
    username: str


class PostBaseResponse(BaseResponse):
    title: str
    content: str
    status: str


class UserResponse(UserBaseResponse, SafeBaseModel):
    comments: list[CommentBaseResponse]
    posts: list[PostBaseResponse]


class PostResponse(PostBaseResponse, SafeBaseModel):
    user: UserBaseResponse | None
    comments: list[CommentBaseResponse]
    tags: list[TagBaseResponse]
