import logging
from typing import Any, Awaitable, Callable
from api import health
from config.logging_config import setup_logging
from fastapi import FastAPI, Response, Request

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


app.include_router(health.router)
