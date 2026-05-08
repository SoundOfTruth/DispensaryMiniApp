from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.params import PaginationParams, QueryIds
from src.schemas.inspections import CreateInspectionSchema, UpdateInspectionSchema
from src.services.inspections import InspectionServiceDep

router = APIRouter(prefix="/inspections", tags=["Inspections"])


@router.get("/")
async def get_inspections(
    service: InspectionServiceDep,
    pagination: Annotated[PaginationParams, Depends()],
    search: str | None = None,
):
    return await service.get_all(
        limit=pagination.limit, offset=pagination.offset, search=search
    )


@router.get("/{id}/")
async def get_inspection(service: InspectionServiceDep, id: int):
    return await service.get(id)


@router.post("/", status_code=201)
async def create_inspection(
    service: InspectionServiceDep, schema: CreateInspectionSchema
):
    return await service.create(schema)


@router.patch("/{id}/")
async def update_inspection(
    service: InspectionServiceDep, id: int, schema: UpdateInspectionSchema
):
    return await service.update(id, schema)


@router.delete("/bulk/", status_code=204)
async def delete_doctors(service: InspectionServiceDep, ids: QueryIds):
    return await service.bulk_delete(ids)


@router.delete("/{id}/", status_code=204)
async def delete_doctor(service: InspectionServiceDep, id: int):
    return await service.delete(id)
