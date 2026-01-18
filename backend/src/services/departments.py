from typing import Annotated

from fastapi import Depends

from src.api.exceptions import NotFoundException
from src.database.core import AsyncScopedSessionDep
from src.repositories.departments import DepartmentRepository
from src.schemas.departments import CreateDepartmentShema, DepartmentSchema


class DepartmentService:
    def __init__(self, session: AsyncScopedSessionDep):
        self.department_rep = DepartmentRepository(session)

    async def get(self, id: int) -> DepartmentSchema:
        department = await self.department_rep.get(id)
        if not department:
            raise NotFoundException
        return DepartmentSchema.model_validate(department)

    async def get_all(self) -> list[DepartmentSchema]:
        departments = await self.department_rep.get_all()
        return [
            DepartmentSchema.model_validate(department) for department in departments
        ]

    async def create(self, schema: CreateDepartmentShema) -> DepartmentSchema:
        payload = schema.model_dump()
        department = await self.department_rep.create(payload)
        return DepartmentSchema.model_validate(department)


DepartmentServiceDep = Annotated[DepartmentService, Depends(DepartmentService)]
