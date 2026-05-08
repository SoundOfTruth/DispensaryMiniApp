from typing import Annotated

from fastapi import Depends

from src.database.core import AsyncScopedSessionDep
from src.repositories.users import UserRepository
from src.schemas.auth import LoginUserSchema, TokenResponse, TokenType
from src.schemas.users import UserSchema
from src.services.exceptions import LoginError, UnauthenticatedError
from src.utils.auth import (
    create_access_token,
    create_refresh_token,
    get_token_data,
    verify_password,
)


class JwtAuthService:
    def __init__(self, session: AsyncScopedSessionDep) -> None:
        self.user_rep = UserRepository(session)

    async def create(self, schema: LoginUserSchema):
        user_db = await self.user_rep.get_by_email(schema.email)
        if not user_db or not verify_password(schema.password, user_db.password):
            raise LoginError
        user_schema = UserSchema.model_validate(user_db)
        access_token = create_access_token(user_schema)
        refresh_token = create_refresh_token(user_schema)
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def refresh(self, refresh_token: str):
        token_data = get_token_data(refresh_token)
        if token_data.type != TokenType.refresh.value:
            raise UnauthenticatedError
        user_db = await self.user_rep.get(token_data.sub)
        if not user_db:
            raise UnauthenticatedError
        user_schema = UserSchema.model_validate(user_db)
        access_token = create_access_token(user_schema)
        return TokenResponse(access_token=access_token)


JwtAuthServiceDep = Annotated[JwtAuthService, Depends(JwtAuthService)]
