from fastapi import APIRouter

from src.schemas.doctors import CreateDoctorSchema
from src.services.doctors import DoctorServiceDep

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.get("/")
async def get_doctors(service: DoctorServiceDep):
    return await service.get_all()


@router.get("/{id}/")
async def get_doctor(service: DoctorServiceDep, id: int):
    return await service.get(id)


@router.post("/")
async def create_doctor(service: DoctorServiceDep, schema: CreateDoctorSchema):
    return await service.create(schema)
