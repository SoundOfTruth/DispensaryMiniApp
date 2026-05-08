from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, PlainSerializer

Sub = Annotated[int, PlainSerializer(lambda val: str(val), return_type=str)]

DateTimeAsTimestamp = Annotated[
    datetime, PlainSerializer(lambda dt: int(dt.timestamp()), return_type=int)
]


class TokenType(Enum):
    refresh = "refresh"
    access = "access"


class TokenDataSchema(BaseModel):
    sub: Sub
    iat: DateTimeAsTimestamp
    exp: DateTimeAsTimestamp
    type: TokenType
    is_superuser: bool = False

    model_config = ConfigDict(extra="allow", use_enum_values=True)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = Field(default=None, exclude=True)
    token_type: str = "Bearer"


class LoginUserSchema(BaseModel):
    email: EmailStr = Field(max_length=254)
    password: str
