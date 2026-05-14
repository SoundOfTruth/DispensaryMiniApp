from pydantic import ConfigDict, EmailStr, Field

from src.schemas.auth import Role
from src.schemas.base import BaseSchema


class CreateUserSchema(BaseSchema):
    email: EmailStr = Field(max_length=254)
    firstname: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    middlename: str = Field(max_length=50)
    password: str = Field(min_length=8)
    role: Role

    model_config = ConfigDict(use_enum_values=True)


class UpdateUserSchema(BaseSchema):
    email: EmailStr = Field("", max_length=254)
    lastname: str = Field("", max_length=50)
    firstname: str = Field("", max_length=50)
    middlename: str = Field("", max_length=50)
    password: str = Field("", min_length=8)
    role: Role = Field(Role.USER)

    model_config = ConfigDict(use_enum_values=True)


class UserSchema(CreateUserSchema):
    id: int
    password: str = Field(exclude=True)

    model_config = ConfigDict(from_attributes=True)


class PasswordChangeSchema(BaseSchema):
    new_password: str = Field(min_length=8)
    current_password: str


class PaginatedUserSchema(BaseSchema):
    count: int
    results: list[UserSchema]
