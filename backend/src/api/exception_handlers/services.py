from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


from src.services.exceptions import (
    EmptyPatchError,
    InvalidFileExtensionError,
    InvalidImageUrlError,
    InvalidPasswordError,
    LoginError,
    NotFoundError,
    UnauthenticatedError,
)

def register_service_exception_handlers(app: FastAPI):
    @app.exception_handler(NotFoundError)
    def handle_not_found(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Страница не найдена."},
        )

    @app.exception_handler(UnauthenticatedError)
    def handle_authentication(request: Request, exc: UnauthenticatedError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Unauthorized."},
        )

    @app.exception_handler(LoginError)
    def handle_login(request: Request, exc: LoginError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Неверный логин или пароль."},
        )

    @app.exception_handler(InvalidFileExtensionError)
    def handle_invalid_file_ext(request: Request, exc: InvalidFileExtensionError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Недопустимый формат файла."},
        )

    @app.exception_handler(EmptyPatchError)
    def handle_empty_patch(request: Request, exc: EmptyPatchError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Ошибка обновления. Nothing to update."},
        )

    @app.exception_handler(InvalidPasswordError)
    def handle_invalid_password(request: Request, exc: InvalidPasswordError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Неверный пароль."},
        )

    @app.exception_handler(InvalidImageUrlError)
    def handle_invalid_image(request: Request, exc: InvalidImageUrlError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Ресурс данного изображения запрещён."},
        )
