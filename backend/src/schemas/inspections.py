from pydantic import ConfigDict

from src.schemas.base import BaseSchema
from src.schemas.doctors import SimpleDoctorSchema


class CreateInspectionSchema(BaseSchema):
    title: str
    description: str
    preparation: str

    doctor_id: int


class InspectionSchema(BaseSchema):
    id: int
    title: str
    description: str
    preparation: str

    doctor: SimpleDoctorSchema

    model_config = ConfigDict(from_attributes=True)
