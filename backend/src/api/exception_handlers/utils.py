from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


from src.utils.exceptions import InvalidTokenSchemaError

def register_utils_exception_handlers(app: FastAPI):
    @app.exception_handler(InvalidTokenSchemaError)
    def handle_invalid_token_create(request: Request, exc: InvalidTokenSchemaError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Ошибка создания токена авторизации."},
        )
