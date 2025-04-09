from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse

app = FastAPI(
    title="FASTAPI+SQLAlchemy+Pydantic",
)


@app.get("/test")
def health() -> Response:
    """Provides a health check of the service."""
    return JSONResponse(content={"message": "Service is healthy!"}, status_code=status.HTTP_200_OK)
