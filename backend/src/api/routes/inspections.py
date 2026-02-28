from fastapi import APIRouter

from src.schemas.inspections import CreateInspectionSchema
from src.services.inspections import InspectionServiceDep

router = APIRouter(prefix="/inspections", tags=["Inspections"])


@router.get("/")
async def get_inspections(service: InspectionServiceDep, search: str | None = None):
    return await service.get_all(search)


@router.get("/{id}/")
async def get_inspection(service: InspectionServiceDep, id: int):
    return await service.get(id)


@router.post("/")
async def create_inspection(
    service: InspectionServiceDep, schema: CreateInspectionSchema
):
    return await service.create(schema)
