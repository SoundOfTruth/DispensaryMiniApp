from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.api.exceptions import DbIntegrityException, NotFoundException


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(NotFoundException)
    def handle_not_found(request: Request, exc: NotFoundException):
        message = "Страница не найдена."
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": message}
        )

    @app.exception_handler(DbIntegrityException)
    def handle_db_integrity(request: Request, exc: DbIntegrityException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": exc.detail}
        )
