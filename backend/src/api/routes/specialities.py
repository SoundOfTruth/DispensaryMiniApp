from fastapi import APIRouter, Depends

from src.api.dependencies import has_admin_permissions
from src.api.params import QueryIds
from src.schemas.specialities import CreateSpecialitySchema, UpdateSpecialitySchema
from src.services.specialities import SpecialityServiceDep

router = APIRouter(
    prefix="/specialties",
    tags=["Specialties"],
)


@router.get("/")
async def get_specialties(service: SpecialityServiceDep):
    return await service.get_all()


@router.get("/{id}/")
async def get_speciality(service: SpecialityServiceDep, id: int):
    return await service.get(id)


@router.post("/", status_code=201, dependencies=[Depends(has_admin_permissions)])
async def create_speciality(
    service: SpecialityServiceDep, schema: CreateSpecialitySchema
):
    return await service.create(schema)


@router.put("/{id}/", dependencies=[Depends(has_admin_permissions)])
async def update_speciality(
    service: SpecialityServiceDep, id: int, schema: UpdateSpecialitySchema
):
    return await service.update(id, schema)


@router.delete("/bulk/", status_code=204, dependencies=[Depends(has_admin_permissions)])
async def delete_specialties(service: SpecialityServiceDep, ids: QueryIds):
    return await service.bulk_delete(ids)


@router.delete("/{id}/", status_code=204, dependencies=[Depends(has_admin_permissions)])
async def delete_specialty(service: SpecialityServiceDep, id: int):
    return await service.delete(id)
