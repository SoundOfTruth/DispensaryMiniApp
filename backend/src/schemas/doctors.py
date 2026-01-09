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


class SimpleDoctorSchema(BaseSchema):
    id: int
    firstname: str
    lastname: str
    middlename: str

    model_config = ConfigDict(from_attributes=True)


class SpecialitySchema(BaseSchema):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class DepartmentSchema(BaseSchema):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class DoctorSchema(SimpleDoctorSchema):
    qualification: str
    experience: int
    speciality: SpecialitySchema
    department: DepartmentSchema

    education: list["EducationSchema"]
    extra_education: list["ExtraEducationShema"]

    @field_serializer("speciality")
    def serialize_speciality(self, obj):
        return obj.name

    @field_serializer("department")
    def serialize_department(self, obj):
        return obj.name


class CreateEducationSchema(BaseSchema):
    title: str


class EducationSchema(CreateEducationSchema):
    id: int


class CreateExtraEducationSchema(EducationSchema):
    pass


class ExtraEducationShema(CreateExtraEducationSchema):
    int: int
