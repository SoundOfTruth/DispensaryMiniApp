from typing import Annotated

from fastapi import APIRouter, Depends, Query

from services.equipment_types import EquipmentTypeServiceDep
from src.api.dependencies import has_admin_permissions
from src.api.params import QueryIds
from src.schemas.equipments import CreateEquipmentTypeSchema, UpdateEquipmentTypeSchema

router = APIRouter(
    prefix="/equipment-types",
    tags=["Equipment Types"],
    dependencies=[Depends(has_admin_permissions)],
)


@router.get("/")
async def get_equipment_types(
    service: EquipmentTypeServiceDep, detail: Annotated[bool | None, Query()] = None
):
    if detail:
        return await service.get_all_with_relations()
    return await service.get_all()


@router.get("/{id}/", dependencies=[])
async def get_equipment_type(service: EquipmentTypeServiceDep, id: int):
    return await service.get(id)


@router.post("/", status_code=201)
async def create_equipment_type(
    service: EquipmentTypeServiceDep,
    schema: CreateEquipmentTypeSchema,
):
    return await service.create(schema)


@router.put("/{id}/")
async def update_equipment_type(
    service: EquipmentTypeServiceDep,
    id: int,
    schema: UpdateEquipmentTypeSchema,
):
    return await service.update(id, schema)


@router.delete("/bulk/", status_code=204)
async def delete_equipment_types(service: EquipmentTypeServiceDep, ids: QueryIds):
    return await service.bulk_delete(ids)


@router.delete("/{id}/", status_code=204)
async def delete_equipment_type(service: EquipmentTypeServiceDep, id: int):
    return await service.delete(id)
