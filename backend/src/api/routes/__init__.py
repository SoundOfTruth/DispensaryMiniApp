from fastapi import APIRouter

from src.api.routes.departments import router as departments_router
from src.api.routes.doctors import router as doctors_router
from src.api.routes.equipments import router as equipments_router
from src.api.routes.inspections import router as inspections_router
from src.api.routes.specialities import router as specialities_router

api_router = APIRouter(prefix="/api")
api_router.include_router(inspections_router)
api_router.include_router(doctors_router)
api_router.include_router(specialities_router)
api_router.include_router(departments_router)
api_router.include_router(equipments_router)
