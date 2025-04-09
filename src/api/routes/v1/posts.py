import logging
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from api.schemas.responses import PostResponse
from container import Container
from models.enums import PostStatus
from services.query import QueryService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/posts", tags=["posts"])

posts_metadata = {
    "name": "posts",
    "description": "functions to manage posts.",
}


@router.get(
    "",
    responses={
        200: {
            "description": "Posts retrieved successfully",
            "model": list[PostResponse],
        },
        500: {
            "500": "Unexpected error occurred during retrieving posts",
            "model": dict[str, str],
        },
    },
)
@inject
async def get_posts(
    status: PostStatus | None = Query(None),
    include: str | None = Query(None),
    post_service: QueryService = Depends(Provide[Container.post_service]),
) -> list[PostResponse]:
    """Ges posts placeholder text."""
    filters = {"status": status} if status else {}
    include = [item.strip() for item in include.split(",")] if include else []
    result = await post_service.get_many(
        filters=filters,
        includes=include,
    )

    return [PostResponse.from_orm_safe(post) for post in result]


@router.get(
    "/{id}",
    responses={
        200: {
            "description": "Post retrieved successfully",
            "model": PostResponse,
        },
        404: {
            "description": "Post not found",
            "model": dict[str, str],
        },
        500: {
            "500": "Unexpected error occurred during retrieving posts",
            "model": dict[str, str],
        },
    },
)
@inject
async def get_post(
    id: UUID,
    include: str | None = None,
    post_service: QueryService = Depends(Provide[Container.post_service]),
) -> PostResponse:
    includes = [item.strip() for item in include.split(",")] if include else []
    result = await post_service.get_one(
        id=id,
        includes=includes,
    )
    return PostResponse.from_orm_safe(result)
