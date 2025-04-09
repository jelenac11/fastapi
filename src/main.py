import logging
from collections.abc import Awaitable
from typing import Any, Callable

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response

from api.routes import health
from api.routes.v1 import posts
from config.error_middleware import errors_config
from config.logging_config import setup_logging
from container import Container
from settings import AppConfig

setup_logging()

logger = logging.getLogger(__name__)

load_dotenv(dotenv_path=".env", override=True)

app = FastAPI(
    title="FASTAPI+SQLAlchemy+Pydantic",
)

container = Container()
container.config.from_pydantic(AppConfig())
app.container = container  # type: ignore


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
app.include_router(posts.router)

errors_config(app)
