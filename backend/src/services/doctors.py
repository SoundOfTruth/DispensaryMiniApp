from typing import Annotated

from fastapi import Depends

from src.database.core import AsyncScopedSessionDep
from src.repositories.doctors import DoctorRepository
from src.schemas.doctors import CreateDoctorSchema, DoctorSchema


class DoctorsService:
    def __init__(self, session: AsyncScopedSessionDep):
        self.doctor_repo = DoctorRepository(session)

    async def get(self, id: int):
        doctor = await self.doctor_repo.get_with_relations(id)
        if not doctor:
            raise
        return DoctorSchema.model_validate(doctor)

    async def get_all(self):
        doctors = await self.doctor_repo.get_all_with_relations()
        return [DoctorSchema.model_validate(doctor) for doctor in doctors]

    async def create(self, schema: CreateDoctorSchema):
        payload = schema.model_dump()
        doctor = await self.doctor_repo.create(payload)
        return doctor


DoctorServiceDep = Annotated[DoctorsService, Depends(DoctorsService)]
