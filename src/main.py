import logging
from typing import Any, Awaitable, Callable
from config.logging_config import setup_logging
from fastapi import FastAPI, Response, status, Request
from fastapi.responses import JSONResponse

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title="FASTAPI+SQLAlchemy+Pydantic",
)


@app.middleware("http")
async def access_log_middleware(request: Request, call_next: Callable[[Request], Awaitable[Any]]) -> Response:
    response: Response = await call_next(request)
    logger.info(
        "Incoming request",
        extra={
            "req": {"method": request.method, "url": str(request.url)},
            "res": {"status_code": response.status_code},
        },
    )
    return response


@app.get("/test")
def health() -> Response:
    """Provides a health check of the service."""
    return JSONResponse(content={"message": "Service is healthy!"}, status_code=status.HTTP_200_OK)
