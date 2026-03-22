from typing import Annotated

from fastapi import Depends

from src.api.exceptions import NotFoundException
from src.database.core import AsyncScopedSessionDep
from src.repositories.doctors import DoctorRepository
from src.schemas.doctors import (
    CreateDoctorSchema,
    DoctorFiltersSchema,
    DoctorSchema,
    PaginatedDoctorSchema,
    SimpleDoctorSchema,
)


class DoctorsService:
    def __init__(self, session: AsyncScopedSessionDep):
        self.doctor_repo = DoctorRepository(session)

    async def get(self, id: int):
        doctor = await self.doctor_repo.get_with_relations(id)
        if not doctor:
            raise NotFoundException
        return DoctorSchema.model_validate(doctor)

    async def get_all(
        self, limit: int, offset: int, search: str | None, filters: DoctorFiltersSchema
    ):
        filters_dict = filters.model_dump(exclude_none=True)
        count = await self.doctor_repo.count(filters_dict, search)
        doctors = await self.doctor_repo.get_all(
            filters=filters_dict,
            search=search,
            offset=offset,
            limit=limit,
        )
        results = [SimpleDoctorSchema.model_validate(doctor) for doctor in doctors]
        return PaginatedDoctorSchema(count=count, results=results)

    async def get_all_with_relations(self):
        doctors = await self.doctor_repo.get_all_with_relations()
        return [DoctorSchema.model_validate(doctor) for doctor in doctors]

    async def create(self, schema: CreateDoctorSchema):
        payload = schema.model_dump()
        education = payload.pop("education")
        extra_education = payload.pop("extra_education")
        doctor = await self.doctor_repo.create(
            payload, education=education, extra_education=extra_education
        )
        return doctor


DoctorServiceDep = Annotated[DoctorsService, Depends()]
