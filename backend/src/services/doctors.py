from typing import Annotated

from fastapi import Depends

from src.database.core import AsyncScopedSessionDep
from src.repositories.doctors import DoctorRepository
from src.schemas.doctors import CreateDoctorSchema, DoctorSchema, SimpleDoctorSchema


class DoctorsService:
    def __init__(self, session: AsyncScopedSessionDep):
        self.doctor_repo = DoctorRepository(session)

    async def get(self, id: int):
        doctor = await self.doctor_repo.get_with_relations(id)
        if not doctor:
            raise
        return DoctorSchema.model_validate(doctor)

    async def get_all(self):
        doctors = await self.doctor_repo.get_all()
        return [SimpleDoctorSchema.model_validate(doctor) for doctor in doctors]

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


DoctorServiceDep = Annotated[DoctorsService, Depends(DoctorsService)]
