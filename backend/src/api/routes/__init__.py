from fastapi import APIRouter

from src.api.routes.auth import router as auth_router
from src.api.routes.departments import router as departments_router
from src.api.routes.doctors import router as doctors_router
from src.api.routes.equipment_types import router as equipment_types_router
from src.api.routes.equipments import router as equipments_router
from src.api.routes.files import router as files_router
from src.api.routes.inspections import router as inspections_router
from src.api.routes.specialities import router as specialties_router
from src.api.routes.users import router as users_router

api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(inspections_router)
api_router.include_router(doctors_router)
api_router.include_router(specialties_router)
api_router.include_router(departments_router)
api_router.include_router(equipments_router)
api_router.include_router(equipment_types_router)
api_router.include_router(files_router)


__all__ = ["api_router"]
