from pydantic import BaseModel, ConfigDict, Field

from src.schemas.doctors import SimpleDoctorSchema


class CreateDoctorInspectionSchema(BaseModel):
    doctor_id: int = Field(alias="id")


class CreateInspectionSchema(BaseModel):
    title: str = Field(max_length=255)
    description: str = Field("", min_length=0)
    preparation: str

    doctors: list[CreateDoctorInspectionSchema]

    model_config = ConfigDict(str_min_length=1, str_max_length=1_000_000)


class UpdateInspectionSchema(BaseModel):
    title: str = Field("", max_length=255, examples=["s"])
    description: str = Field("", examples=["s"])
    preparation: str = Field("", examples=["s"])

    doctors: list[CreateDoctorInspectionSchema] | None = None

    model_config = ConfigDict(str_min_length=1, str_max_length=1_000_000)


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
