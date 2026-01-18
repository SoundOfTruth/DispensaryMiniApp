from fastapi import APIRouter

from src.schemas.specialities import CreateSpecialityShema
from src.services.specialities import SpecialityServiceDep

router = APIRouter(prefix="/specialities", tags=["Specialities"])


@router.get("/")
async def get_specialities(service: SpecialityServiceDep):
    return await service.get_all()


@router.get("/{id}/")
async def get_speciality(service: SpecialityServiceDep, id: int):
    return await service.get(id)


@router.post("/")
async def create_speciality(
    service: SpecialityServiceDep, schema: CreateSpecialityShema
):
    return await service.create(schema)
