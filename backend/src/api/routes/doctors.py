from typing import Annotated

from fastapi import APIRouter, Depends

from src.schemas.doctors import CreateDoctorSchema, DoctorFiltersSchema
from src.schemas.pagination import PaginationParams
from src.services.doctors import DoctorServiceDep

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.get("/")
async def get_doctors(
    service: DoctorServiceDep,
    filters: Annotated[DoctorFiltersSchema, Depends()],
    pagination: Annotated[PaginationParams, Depends()],
    search: str | None = None,
):
    return await service.get_all(
        limit=pagination.limit, offset=pagination.offset, search=search, filters=filters
    )


@router.get("/{id}/")
async def get_doctor(service: DoctorServiceDep, id: int):
    return await service.get(id)


@router.post("/")
async def create_doctor(service: DoctorServiceDep, schema: CreateDoctorSchema):
    return await service.create(schema)
