from typing import Annotated

from fastapi import Depends

from src.database.core import AsyncScopedSessionDep
from src.repositories.departments import DepartmentRepository
from src.schemas.departments import CreateDepartmentSchema, DepartmentSchema
from src.services.exceptions import NotFoundError


class DepartmentService:
    def __init__(self, session: AsyncScopedSessionDep):
        self.department_rep = DepartmentRepository(session)

    async def create(self, schema: CreateDepartmentSchema) -> DepartmentSchema:
        department = await self.department_rep.create(schema.model_dump())
        return DepartmentSchema.model_validate(department)

    async def update(self, id: int, schema: CreateDepartmentSchema):
        department = await self.department_rep.update(id, schema.model_dump())
        if not department:
            raise NotFoundError
        return DepartmentSchema.model_validate(department)

    async def get_all(self) -> list[DepartmentSchema]:
        departments = await self.department_rep.get_all()
        return [
            DepartmentSchema.model_validate(department) for department in departments
        ]

    async def get(self, id: int) -> DepartmentSchema:
        department = await self.department_rep.get(id)
        if not department:
            raise NotFoundError
        return DepartmentSchema.model_validate(department)

    async def delete(self, id: int):
        return await self.department_rep.delete(id)

    async def bulk_delete(self, ids: list[int]):
        return await self.department_rep.bulk_delete(ids)


DepartmentServiceDep = Annotated[DepartmentService, Depends()]
