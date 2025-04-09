import logging
from api.schemas.responses import PostResponse
from fastapi import APIRouter, Query, Depends
from models.enums import PostStatus
from dependency_injector.wiring import Provide, inject
from container import Container
from services.post import PostService

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
    post_service: PostService = Depends(Provide[Container.post_service]),
) -> list[PostResponse]:
    """Ges posts placeholder text."""
    filters = {"status": status} if status else {}
    include = include.split(",") if include else []
    result = await post_service.get(
        filters=filters,
        includes=include,
    )

    return [PostResponse.from_orm_safe(post) for post in result]
