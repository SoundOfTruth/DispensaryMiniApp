from fastapi import APIRouter, Cookie, Response

from config import settings
from src.schemas.auth import LoginUserSchema, TokenResponse
from src.services.auth import JwtAuthServiceDep

router = APIRouter(prefix="/auth", tags=["JWT"])


@router.post("/login/", response_model=TokenResponse)
async def create_jwt(
    service: JwtAuthServiceDep, schema: LoginUserSchema, response: Response
):
    token_schema = await service.create(schema)
    refresh_token = token_schema.refresh_token
    if refresh_token:
        if not settings.DEBUG:
            response.set_cookie(
                key="app_rt",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="strict",
                max_age=604800,
                path="/api/refresh/",
            )
        else:
            response.set_cookie(
                key="app_rt",
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite="lax",
                max_age=604800,
                path="/",
            )
    return token_schema


@router.post("/refresh/", response_model=TokenResponse)
async def refresh_jwt(service: JwtAuthServiceDep, app_rt=Cookie(default=None)):
    return await service.refresh(refresh_token=app_rt)


@router.post("/logout/")
async def logout(response: Response):
    if not settings.DEBUG:
        response.delete_cookie(key="app_rt", path="/api/refresh")
    else:
        response.delete_cookie(key="app_rt", path="/")
