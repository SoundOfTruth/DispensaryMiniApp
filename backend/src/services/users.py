from typing import Annotated

from fastapi import Depends

from src.api.params import PaginationParams
from src.database.core import AsyncScopedSessionDep
from src.repositories.users import UserRepository
from src.schemas.users import (
    CreateUserSchema,
    PaginatedUserSchema,
    UpdateUserSchema,
    UserSchema,
)
from src.services.exceptions import EmptyPatchError, InvalidPasswordError, NotFoundError
from src.utils.auth import hash_password, verify_password


class UserService:
    def __init__(self, session: AsyncScopedSessionDep) -> None:
        self.user_rep = UserRepository(session)

    async def create(self, schema: CreateUserSchema) -> UserSchema:
        schema.password = hash_password(schema.password)
        user = await self.user_rep.create(schema.model_dump())
        return UserSchema.model_validate(user)

    async def update(self, id: int, schema: UpdateUserSchema) -> UserSchema:
        payload = schema.model_dump(exclude_unset=True)
        if not payload:
            raise EmptyPatchError
        new_password = payload.get("password")
        if new_password:
            payload["password"] = hash_password(new_password)
        user = await self.user_rep.update(id, payload)
        if not user:
            raise NotFoundError
        return UserSchema.model_validate(user)

    async def get_all(
        self,
        pagination: PaginationParams,
        search: str | None,
    ):
        users = await self.user_rep.get_all(
            search=search, limit=pagination.limit, offset=pagination.offset
        )
        count = await self.user_rep.count(search=search)
        results = [UserSchema.model_validate(user) for user in users]
        return PaginatedUserSchema(results=results, count=count)

    async def get(self, id: int) -> UserSchema:
        user = await self.user_rep.get(id)
        if not user:
            raise NotFoundError
        return UserSchema.model_validate(user)

    async def get_by_email(self, email: str):
        user = await self.user_rep.get_by_email(email)
        if not user:
            raise NotFoundError
        return UserSchema.model_validate(user)

    async def change_password(
        self,
        user_id: int,
        current_password: str,
        new_password: str,
    ):
        user = await self.get(user_id)
        if not user:
            raise FileNotFoundError
        if not verify_password(current_password, user.password):
            raise InvalidPasswordError
        await self.user_rep.change_password(user_id, hash_password(new_password))

    async def delete(self, id: int):
        return await self.user_rep.delete(id)

    async def bulk_delete(self, ids: list[int]):
        return await self.user_rep.bulk_delete(ids)


UserServiceDep = Annotated[UserService, Depends()]
