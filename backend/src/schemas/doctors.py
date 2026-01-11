from pydantic import ConfigDict, field_serializer

from src.schemas.base import BaseSchema


class CreateDoctorSchema(BaseSchema):
    firstname: str
    lastname: str
    middlename: str
    qualification: str
    experience_start: int
    speciality_id: int
    department_id: int

    education: list[str]
    extra_education: list[str]


class SimpleDoctorSchema(BaseSchema):
    id: int
    firstname: str
    lastname: str
    middlename: str
    qualification: str | None
    speciality: "SpecialitySchema | None"
    department: "DepartmentSchema"

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("speciality")
    def serialize_speciality(self, obj):
        return obj.name

    @field_serializer("department")
    def serialize_department(self, obj):
        return obj.name


class SpecialitySchema(BaseSchema):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class DepartmentSchema(BaseSchema):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class DoctorSchema(SimpleDoctorSchema):
    experience: int | None

    education: list["EducationSchema"]
    extra_education: list["ExtraEducationSchema"]

    @field_serializer("education")
    def serialize_education(self, obj: list["EducationSchema"]):
        return [row.title for row in obj]

    @field_serializer("extra_education")
    def serialize_extra_education(self, obj: list["ExtraEducationSchema"]):
        return [row.title for row in obj]


class CreateEducationSchema(BaseSchema):
    title: str
    doctor_id: int


class EducationSchema(CreateEducationSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CreateExtraEducationSchema(CreateEducationSchema):
    pass


class ExtraEducationSchema(CreateExtraEducationSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
