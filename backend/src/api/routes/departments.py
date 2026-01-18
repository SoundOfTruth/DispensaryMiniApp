from fastapi import APIRouter

from src.schemas.departments import CreateDepartmentShema
from src.services.departments import DepartmentServiceDep

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("/")
async def get_departments(service: DepartmentServiceDep):
    return await service.get_all()


@router.get("/{id}/")
async def get_department(service: DepartmentServiceDep, id: int):
    return await service.get(id)


@router.post("/")
async def create_department(
    service: DepartmentServiceDep, schema: CreateDepartmentShema
):
    return await service.create(schema)
