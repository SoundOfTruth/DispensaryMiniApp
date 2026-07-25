from typing import Annotated

from fastapi import Depends

from src.cache.manager import CacheManager
from src.database.core import AsyncScopedSessionDep
from src.repositories.departments import DepartmentRepository
from src.schemas.departments import CreateDepartmentSchema, DepartmentSchema
from src.services.exceptions import NotFoundError

cache = CacheManager("department")


class DepartmentService:
    def __init__(self, session: AsyncScopedSessionDep):
        self.department_rep = DepartmentRepository(session)

    @cache.expire
    async def create(self, schema: CreateDepartmentSchema) -> DepartmentSchema:
        department = await self.department_rep.create(schema.model_dump())
        return DepartmentSchema.model_validate(department)

    @cache.expire
    async def update(self, id: int, schema: CreateDepartmentSchema) -> DepartmentSchema:
        department = await self.department_rep.update(id, schema.model_dump())
        if not department:
            raise NotFoundError
        return DepartmentSchema.model_validate(department)

    @cache.use
    async def get_all(self, search: str | None) -> list[DepartmentSchema]:
        departments = await self.department_rep.get_all(search=search)
        return [
            DepartmentSchema.model_validate(department) for department in departments
        ]

    @cache.use
    async def get(self, id: int) -> DepartmentSchema:
        department = await self.department_rep.get(id)
        if not department:
            raise NotFoundError
        return DepartmentSchema.model_validate(department)

    @cache.expire
    async def delete(self, id: int):
        return await self.department_rep.delete(id)


DepartmentServiceDep = Annotated[DepartmentService, Depends()]
