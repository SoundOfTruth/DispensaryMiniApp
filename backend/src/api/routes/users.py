from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.api.dependencies import AccessTokenDep
from src.api.params import PaginationParams, QueryIds
from src.schemas.users import CreateUserSchema, PasswordChangeSchema, UpdateUserSchema
from src.services.users import UserServiceDep

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(service: UserServiceDep, schema: CreateUserSchema):
    return await service.create(schema)


@router.patch("/{id}/")
async def update_user(service: UserServiceDep, id: int, schema: UpdateUserSchema):
    return await service.update(id, schema)


@router.get("/")
async def get_users(
    service: UserServiceDep,
    pagination: Annotated[PaginationParams, Depends()],
    search: str | None = None,
):
    return await service.get_all(pagination, search)


@router.get("/me/")
async def get_me(service: UserServiceDep, token: AccessTokenDep):
    return await service.get(token.sub)


@router.get("/{id}/")
async def get_user(service: UserServiceDep, id: int):
    return await service.get(id)


@router.post("/change_password/")
async def change_password(
    service: UserServiceDep, schema: PasswordChangeSchema, token: AccessTokenDep
):
    await service.change_password(
        token.sub, schema.current_password, schema.new_password
    )


@router.delete("/bulk/", status_code=204)
async def delete_speciality(service: UserServiceDep, ids: QueryIds):
    return await service.bulk_delete(ids)


@router.delete("/{id}/", status_code=204)
async def delete_specialties(service: UserServiceDep, id: int):
    return await service.delete(id)
