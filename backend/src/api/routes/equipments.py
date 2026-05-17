from fastapi import APIRouter, Depends, Request

from src.api.dependencies import has_admin_permissions, has_superuser_permissions
from src.api.params import QueryIds
from src.schemas.equipments import CreateEquipmentSchema, UpdateEquipmentSchema
from src.services.equipments import EquipmentServiceDep

router = APIRouter(
    prefix="/equipments",
    tags=["Equipments"],
    dependencies=[Depends(has_admin_permissions)],
)


@router.get("/")
async def get_equiments(service: EquipmentServiceDep, search: str | None = None):
    return await service.get_all(search)


@router.get("/{id}/")
async def get_equipment(service: EquipmentServiceDep, id: int):
    return await service.get(id)


@router.post("/", status_code=201)
async def create_equipment(
    service: EquipmentServiceDep, schema: CreateEquipmentSchema, request: Request
):
    return await service.create(schema, str(request.base_url))


@router.patch("/{id}/")
async def update_equipment(
    service: EquipmentServiceDep,
    id: int,
    schema: UpdateEquipmentSchema,
    request: Request,
):
    return await service.update(id, schema, str(request.base_url))


@router.delete(
    "/bulk/", status_code=204, dependencies=[Depends(has_superuser_permissions)]
)
async def delete_equipments(service: EquipmentServiceDep, ids: QueryIds):
    return await service.bulk_delete(ids)


@router.delete(
    "/{id}/", status_code=204, dependencies=[Depends(has_superuser_permissions)]
)
async def delete_equipment(service: EquipmentServiceDep, id: int):
    return await service.delete(id)
