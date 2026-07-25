from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import has_admin_permissions
from src.api.params import PaginationParams
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


@router.post("/", status_code=201, dependencies=[Depends(has_admin_permissions)])
async def create_doctor(service: DoctorServiceDep, schema: CreateDoctorSchema):
    return await service.create(schema)


@router.patch("/{id}/", dependencies=[Depends(has_admin_permissions)])
async def update_doctor(service: DoctorServiceDep, id: int, schema: UpdateDoctorSchema):
    return await service.update(id, schema)


@router.delete("/{id}/", status_code=204, dependencies=[Depends(has_admin_permissions)])
async def delete_doctor(service: DoctorServiceDep, id: int):
    return await service.delete(id)
