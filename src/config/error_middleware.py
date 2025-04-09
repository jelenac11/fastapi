from fastapi import FastAPI

from exceptions.custom_exception_handlers import CustomExceptionHandler
from exceptions.custom_exceptions import NotFoundError


def errors_config(app: FastAPI) -> None:
    custom_exception_handler = CustomExceptionHandler()

    app.exception_handler(NotFoundError)(
        custom_exception_handler.not_found_error_handler,
    )
