from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/health", tags=["health"])

health_metadata = {
    "name": "health",
    "description": "used to check the status of the service. test endpoints.",
}


@router.get("")
def health() -> Response:
    """Provides a health check of the service."""
    return JSONResponse(content={"message": "Service is healthy!"}, status_code=status.HTTP_200_OK)
