from fastapi import APIRouter, Cookie, Response

from src.config import settings
from src.schemas.auth import LoginUserSchema
from src.services.auth import JwtAuthServiceDep

router = APIRouter(prefix="/auth", tags=["JWT"])


@router.post("/login/")
async def create_jwt(
    service: JwtAuthServiceDep, schema: LoginUserSchema, response: Response
):
    token_schema = await service.create(schema)
    refresh_token = token_schema.refresh_token
    if refresh_token:
        if settings.DEBUG:
            response.set_cookie(
                key="app_rt",
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite="lax",
                max_age=604800,
                path="/",
            )
        else:
            response.set_cookie(
                key="app_rt",
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite="strict",
                max_age=604800,
                path="/api/auth/refresh/",
            )
    return token_schema


@router.post("/refresh/")
async def refresh_jwt(service: JwtAuthServiceDep, app_rt=Cookie(default=None)):
    return await service.refresh(refresh_token=app_rt)


@router.post("/logout/")
async def logout(response: Response):
    if settings.DEBUG:
        response.delete_cookie(key="app_rt", path="/")
    else:
        response.delete_cookie(key="app_rt", path="/api/auth/refresh/")
