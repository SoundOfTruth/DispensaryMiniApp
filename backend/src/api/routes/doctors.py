from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.params import PaginationParams, QueryIds
from src.schemas.doctors import (
    CreateDoctorSchema,
    DoctorFiltersSchema,
    UpdateDoctorSchema,
)
from src.services.doctors import DoctorServiceDep

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.get("/")
async def get_doctors(
    service: DoctorServiceDep,
    filters: Annotated[DoctorFiltersSchema, Depends()],
    pagination: Annotated[PaginationParams, Depends()],
    search: str | None = None,
):
    return await service.get_all(pagination=pagination, search=search, filters=filters)


@router.get("/{id}/")
async def get_doctor(service: DoctorServiceDep, id: int):
    return await service.get(id)


@router.post("/", status_code=201)
async def create_doctor(service: DoctorServiceDep, schema: CreateDoctorSchema):
    return await service.create(schema)


@router.patch("/{id}/")
async def update_doctor(service: DoctorServiceDep, id: int, schema: UpdateDoctorSchema):
    return await service.update(id, schema)


@router.delete("/bulk/", status_code=204)
async def delete_doctors(service: DoctorServiceDep, ids: QueryIds):
    return await service.bulk_delete(ids)


@router.delete("/{id}/", status_code=204)
async def delete_doctor(service: DoctorServiceDep, id: int):
    return await service.delete(id)
