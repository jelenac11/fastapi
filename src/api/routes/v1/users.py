import logging
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from api.schemas.responses import UserResponse
from container import Container
from services.query import QueryService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/users", tags=["users"])

users_metadata = {
    "name": "users",
    "description": "functions to retrieve users.",
}


@router.get(
    "/{id}",
    responses={
        200: {
            "description": "User retrieved successfully",
            "model": UserResponse,
        },
        404: {
            "description": "User not found",
            "model": dict[str, str],
        },
        500: {
            "500": "Unexpected error occurred during retrieving user",
            "model": dict[str, str],
        },
    },
)
@inject
async def get_user(
    id: UUID,
    include: str | None = None,
    user_service: QueryService = Depends(Provide[Container.user_service]),
) -> UserResponse:
    includes = [item.strip() for item in include.split(",")] if include else []
    result = await user_service.get_one(
        id=id,
        includes=includes,
    )
    return UserResponse.from_orm_safe(result)
