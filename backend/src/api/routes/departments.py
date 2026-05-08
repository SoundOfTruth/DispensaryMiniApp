from fastapi import APIRouter

from src.api.params import QueryIds
from src.schemas.departments import CreateDepartmentSchema
from src.services.departments import DepartmentServiceDep

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("/")
async def get_departments(service: DepartmentServiceDep):
    return await service.get_all()


@router.get("/{id}/")
async def get_department(service: DepartmentServiceDep, id: int):
    return await service.get(id)


@router.post("/", status_code=201)
async def create_department(
    service: DepartmentServiceDep, schema: CreateDepartmentSchema
):
    return await service.create(schema)


@router.put("/{id}/")
async def update_department(
    service: DepartmentServiceDep, id: int, schema: CreateDepartmentSchema
):
    return await service.update(id, schema)


@router.delete("/bulk/", status_code=204)
async def delete_departments(service: DepartmentServiceDep, ids: QueryIds):
    return await service.bulk_delete(ids)


@router.delete("/{id}/", status_code=204)
async def delete_department(service: DepartmentServiceDep, id: int):
    return await service.delete(id)
