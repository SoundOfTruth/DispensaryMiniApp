from fastapi import APIRouter, Depends

from src.api.dependencies import has_admin_permissions
from src.schemas.equipments import CreateEquipmentSchema, UpdateEquipmentSchema
from src.services.equipments import EquipmentServiceDep

router = APIRouter(
    prefix="/equipments",
    tags=["Equipments"],
)


@router.get("/")
async def get_equiments(service: EquipmentServiceDep, search: str | None = None):
    return await service.get_all(search)


@router.get("/{id}/")
async def get_equipment(service: EquipmentServiceDep, id: int):
    return await service.get(id)


@router.post("/", status_code=201, dependencies=[Depends(has_admin_permissions)])
async def create_equipment(service: EquipmentServiceDep, schema: CreateEquipmentSchema):
    return await service.create(schema)


@router.patch("/{id}/", dependencies=[Depends(has_admin_permissions)])
async def update_equipment(
    service: EquipmentServiceDep,
    id: int,
    schema: UpdateEquipmentSchema,
):
    return await service.update(id, schema)

@router.delete("/{id}/", status_code=204, dependencies=[Depends(has_admin_permissions)])
async def delete_equipment(service: EquipmentServiceDep, id: int):
    return await service.delete(id)
