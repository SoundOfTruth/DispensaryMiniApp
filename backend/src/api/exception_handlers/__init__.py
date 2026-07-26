import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.api.exception_handlers.api import register_api_exception_handlers
from src.api.exception_handlers.repositories import register_repositories_exception_handlers
from src.api.exception_handlers.services import register_service_exception_handlers
from src.api.exception_handlers.utils import register_utils_exception_handlers


log = logging.getLogger("error_handler")


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    def handle_unexpected_err(request: Request, exc: Exception) -> JSONResponse:
        log.exception("Unexpected error", exc_info=exc)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "detail": "Непредвиденная ошибка.",
            },
        )
    register_api_exception_handlers(app)
    register_service_exception_handlers(app)
    register_repositories_exception_handlers(app)
    register_utils_exception_handlers(app)


__all__ = ["add_exception_handlers"]
