from typing import Annotated

from fastapi import APIRouter, Depends

from src.schemas.doctors import CreateDoctorSchema, DoctorFilterParams
from src.services.doctors import DoctorServiceDep

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.get("/")
async def get_doctors(
    service: DoctorServiceDep,
    params: Annotated[DoctorFilterParams, Depends()],
    search: str | None = None,
):
    return await service.get_all(params, search)


@router.get("/{id}/")
async def get_doctor(service: DoctorServiceDep, id: int):
    return await service.get(id)


@router.post("/")
async def create_doctor(service: DoctorServiceDep, schema: CreateDoctorSchema):
    return await service.create(schema)
