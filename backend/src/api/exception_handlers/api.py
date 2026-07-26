from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.api.exceptions import (
    IssuedExcessUserPermissionsError,
    PermissionDeniedError,
    UpdateSelfPasswordError,
    UserSelfDeleteError,
)

def register_api_exception_handlers(app: FastAPI):
    @app.exception_handler(IssuedExcessUserPermissionsError)
    def handle_excess_users_permission(
        request: Request, exc: IssuedExcessUserPermissionsError
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Вы не можете выдать права, превышающие ваши."},
        )

    @app.exception_handler(UserSelfDeleteError)
    def handle_self_delete(request: Request, exc: UserSelfDeleteError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Вы не можете удалить свой аккаунт."},
        )

    @app.exception_handler(UpdateSelfPasswordError)
    def handle_admin_update_password(request: Request, exc: UpdateSelfPasswordError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Сменить свой пароль вы можете только в профиле."},
        )

    @app.exception_handler(PermissionDeniedError)
    def handle_permissions(request: Request, exc: PermissionDeniedError):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Недостаточно прав."},
        )
