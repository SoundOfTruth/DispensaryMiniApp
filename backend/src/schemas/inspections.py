from pydantic import BaseModel, ConfigDict, Field

from src.schemas.doctors import SimpleDoctorSchema


class CreateDoctorInspectionSchema(BaseModel):
    id: int = Field(examples=[1])


class CreateInspectionSchema(BaseModel):
    title: str
    description: str
    preparation: str

    doctors: list[CreateDoctorInspectionSchema]


class InspectionSchema(BaseModel):
    id: int
    title: str
    description: str
    preparation: str

    doctors: list[SimpleDoctorSchema]

    model_config = ConfigDict(from_attributes=True)
