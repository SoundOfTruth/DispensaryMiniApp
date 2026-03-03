from typing import Annotated

from fastapi import APIRouter, Depends

from src.schemas.inspections import CreateInspectionSchema
from src.schemas.pagination import PaginationParams
from src.services.inspections import InspectionServiceDep

router = APIRouter(prefix="/inspections", tags=["Inspections"])


@router.get("/")
async def get_inspections(
    service: InspectionServiceDep,
    pagination: Annotated[PaginationParams, Depends()],
    search: str | None = None,
):
    return await service.get_all(pagination.page, search)


@router.get("/{id}/")
async def get_inspection(service: InspectionServiceDep, id: int):
    return await service.get(id)


@router.post("/")
async def create_inspection(
    service: InspectionServiceDep, schema: CreateInspectionSchema
):
    return await service.create(schema)
