from fastapi import APIRouter

from src.api.params import QueryIds
from src.schemas.equipments import CreateEquipmentSchema, UpdateEquipmentSchema
from src.services.equipments import EquipmentServiceDep

router = APIRouter(prefix="/equipments", tags=["Equipments"])


@router.get("/")
async def get_equiments(service: EquipmentServiceDep):
    return await service.get_all()


@router.get("/{id}/")
async def get_equipment(id: int, service: EquipmentServiceDep):
    return await service.get(id)


@router.post("/", status_code=201)
async def create_equipment(schema: CreateEquipmentSchema, service: EquipmentServiceDep):
    return await service.create(schema)


@router.patch("/{id}/", status_code=201)
async def update_equipment(
    id: int, schema: UpdateEquipmentSchema, service: EquipmentServiceDep
):
    return await service.update(id, schema)


@router.delete("/bulk/", status_code=204)
async def delete_equipments(service: EquipmentServiceDep, ids: QueryIds):
    return await service.bulk_delete(ids)


@router.delete("/{id}/", status_code=204)
async def delete_equipment(service: EquipmentServiceDep, id: int):
    return await service.delete(id)
