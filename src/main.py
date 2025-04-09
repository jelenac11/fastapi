import logging
from typing import Any, Awaitable, Callable
from api.routes import health
from api.routes.v1 import posts
from config.logging_config import setup_logging
from fastapi import FastAPI, Response, Request
from dotenv import load_dotenv
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
