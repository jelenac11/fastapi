from fastapi import Request, status
from fastapi.responses import JSONResponse

from exceptions.custom_exceptions import NotFoundError


class CustomExceptionHandler:
    async def not_found_error_handler(
        self,
        _: Request,
        exc: NotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": f"{exc.message}"},
        )
