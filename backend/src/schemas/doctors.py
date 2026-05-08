from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from src.schemas.base import BaseSchema


class CreateEducationSchema(BaseModel):
    title: str


class CreateExtraEducationSchema(BaseModel):
    title: str


class EducationSchema(CreateEducationSchema):
    model_config = ConfigDict(from_attributes=True)


class ExtraEducationSchema(CreateExtraEducationSchema):
    model_config = ConfigDict(from_attributes=True)


class CreateDoctorInspectionSchema(BaseModel):
    inspection_id: int = Field(alias="id")


class SpecialitySchema(BaseSchema):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class DepartmentSchema(BaseSchema):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class CreateDoctorSchema(BaseModel):
    firstname: str
    lastname: str
    middlename: str
    qualification: str | None
    experience_start: int | None = Field(None, examples=[2000])
    photo: str | None = None

    speciality_id: int = Field(examples=[1])
    department_id: int = Field(examples=[1])

    inspections: list[CreateDoctorInspectionSchema] = Field(examples=[[]])
    education: list[str]
    extra_education: list[str]

    model_config = ConfigDict(str_min_length=1)


class UpdateDoctorSchema(BaseModel):
    firstname: str = Field("")
    lastname: str = Field("")
    middlename: str = Field("")
    qualification: str | None = Field(None)
    experience_start: int | None = Field(None, gt=1920, le=datetime.now().year)
    photo: str | None = None

    speciality_id: int = Field(1)
    department_id: int = Field(1)

    inspections: list[CreateDoctorInspectionSchema] = Field([], examples=[[]])
    education: list[str] = Field([])
    extra_education: list[str] | None = Field([])

    model_config = ConfigDict(str_min_length=1)


class SimpleDoctorSchema(BaseModel):
    id: int
    firstname: str
    lastname: str
    middlename: str
    qualification: str | None
    photo: str | None
    speciality: "SpecialitySchema"
    department: "DepartmentSchema"

    model_config = ConfigDict(from_attributes=True)


class SimpleInspectionSchema(BaseSchema):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)


class DoctorSchema(SimpleDoctorSchema):
    experience_start: int | None
    experience_years: int | None

    education: list["EducationSchema"]
    extra_education: list["ExtraEducationSchema"]
    inspections: list[SimpleInspectionSchema]

    @field_serializer("education")
    def serialize_education(self, obj: list["EducationSchema"]):
        return [row.title for row in obj]

    @field_serializer("extra_education")
    def serialize_extra_education(self, obj: list["ExtraEducationSchema"]):
        return [row.title for row in obj]


class DoctorFiltersSchema(BaseModel):
    speciality_id: int | None = None
    department_id: int | None = None


class PaginatedDoctorSchema(BaseModel):
    count: int
    results: list[SimpleDoctorSchema]
