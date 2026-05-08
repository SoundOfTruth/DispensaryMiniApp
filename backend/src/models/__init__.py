from src.models.doctors import (
    Department,
    Doctor,
    DoctorInspection,
    Education,
    ExtraEducation,
    Speciality,
)
from src.models.equipments import Equipment, EquipmentType
from src.models.inspections import Inspection
from src.models.users import User

__all__ = [
    "Doctor",
    "Education",
    "ExtraEducation",
    "Speciality",
    "Department",
    "Inspection",
    "DoctorInspection",
    "Equipment",
    "EquipmentType",
    "User",
]
