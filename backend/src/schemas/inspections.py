from pydantic import BaseModel, ConfigDict, Field

from src.schemas.base import BaseSchema
from src.schemas.doctors import SimpleDoctorSchema


class CreateDoctorInspectionSchema(BaseModel):
    doctor_id: int = Field(alias="id")


class CreateInspectionSchema(BaseSchema):
    title: str = Field(max_length=255)
    description: str = Field(min_length=0, max_length=200_000)
    preparation: str = Field(min_length=0, max_length=200_000)

    doctors: list[CreateDoctorInspectionSchema] = Field(examples=[[]])


class UpdateInspectionSchema(BaseSchema):
    title: str = Field("", max_length=255, examples=["s"])
    description: str = Field("", examples=["s"], min_length=0, max_length=200_000)
    preparation: str = Field("", examples=["s"], min_length=0, max_length=200_000)

    doctors: list[CreateDoctorInspectionSchema] = []


class SimpleInspectionSchema(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)


class InspectionSchema(SimpleInspectionSchema):
    description: str
    preparation: str

    doctors: list[SimpleDoctorSchema] | None = None

    model_config = ConfigDict(from_attributes=True)


class PaginatedInspectionSchema(BaseModel):
    count: int
    results: list[SimpleInspectionSchema]
