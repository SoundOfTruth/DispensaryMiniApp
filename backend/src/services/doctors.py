from typing import Annotated

from fastapi import Depends

from src.api.params import PaginationParams
from src.database.core import AsyncScopedSessionDep
from src.repositories.doctors import DoctorRepository
from src.schemas.doctors import (
    CreateDoctorSchema,
    DoctorFiltersSchema,
    DoctorSchema,
    PaginatedDoctorSchema,
    SimpleDoctorSchema,
    UpdateDoctorSchema,
)
from src.services.exceptions import EmptyPatchError, NotFoundError


class DoctorService:
    def __init__(self, session: AsyncScopedSessionDep):
        self.doctor_rep = DoctorRepository(session)

    async def create(self, schema: CreateDoctorSchema):
        doctor = await self.doctor_rep.create(schema.model_dump())
        return DoctorSchema.model_validate(doctor)

    async def update(self, id: int, schema: UpdateDoctorSchema):
        payload = schema.model_dump(exclude_unset=True)
        if not payload:
            raise EmptyPatchError
        doctor = await self.doctor_rep.update(id, payload)
        if not doctor:
            raise NotFoundError
        return DoctorSchema.model_validate(doctor)

    async def get_all(
        self,
        pagination: PaginationParams,
        search: str | None,
        filters: DoctorFiltersSchema,
    ):
        filters_dict = filters.model_dump(exclude_none=True)
        count = await self.doctor_rep.count(filters_dict, search)
        doctors = await self.doctor_rep.get_all(
            filters=filters_dict,
            search=search,
            offset=pagination.offset,
            limit=pagination.limit,
        )
        results = [SimpleDoctorSchema.model_validate(doctor) for doctor in doctors]
        return PaginatedDoctorSchema(count=count, results=results)

    async def get(self, id: int):
        doctor = await self.doctor_rep.get_with_relations(id)
        if not doctor:
            raise NotFoundError
        return DoctorSchema.model_validate(doctor)

    async def delete(self, id: int):
        return await self.doctor_rep.delete(id)

    async def bulk_delete(self, ids: list[int]):
        return await self.doctor_rep.bulk_delete(ids)


DoctorServiceDep = Annotated[DoctorService, Depends()]
