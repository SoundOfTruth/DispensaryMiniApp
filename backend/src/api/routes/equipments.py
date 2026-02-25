from typing import Annotated

from fastapi import APIRouter, Query

from src.schemas.equipments import CreateEquipmentSchema, CreateEquipmentTypeSchema
from src.services.equipments import EquipmentServiceDep

router = APIRouter(prefix="/equipments", tags=["Equipments"])


@router.get("/")
async def get_equiments(
    service: EquipmentServiceDep, group_by: Annotated[str | None, Query()] = None
):
    if group_by == "type":
        return await service.get_all_grouped_by_type()
    return await service.get_all()


@router.get("/id/")
async def get_equipment(id: int, service: EquipmentServiceDep):
    return await service.get(id)


@router.post("/")
async def create_equipment(schema: CreateEquipmentSchema, service: EquipmentServiceDep):
    return await service.create(schema)


@router.post("/types/")
async def create_equipment_type(
    schema: CreateEquipmentTypeSchema, service: EquipmentServiceDep
):
    return await service.create_type(schema)


@router.get("/types/")
async def get_types(service: EquipmentServiceDep):
    return await service.get_types()


@router.get("/types/{id}/")
async def get_type(id: int, service: EquipmentServiceDep):
    return await service.get_type(id)
