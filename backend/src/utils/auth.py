from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError
from pydantic import ValidationError

from src.config import settings
from src.schemas.auth import TokenDataSchema, TokenType
from src.schemas.users import UserSchema
from src.services.exceptions import UnauthenticatedError
from src.utils.exceptions import InvalidTokenSchemaError

password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return password_hash.verify(plain_password, hashed_password)
    except UnknownHashError:
        return False


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def encode_jwt(data: dict) -> str:
    return jwt.encode(data, settings.SECRET, settings.ALGORITM)


def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET, [settings.ALGORITM])
    except jwt.exceptions.PyJWTError:
        raise UnauthenticatedError


def create_jwt_token(
    schema: UserSchema, token_type: TokenType, expire_timedelta: timedelta
) -> str:
    iat = datetime.now(timezone.utc)
    exp = iat + expire_timedelta
    try:
        token_schema = TokenDataSchema(
            sub=schema.id,
            iat=iat,
            exp=exp,
            type=token_type,
            role=schema.role,
        )
    except ValidationError:
        raise InvalidTokenSchemaError
    else:
        return encode_jwt(token_schema.model_dump())


def get_token_data(token: str) -> TokenDataSchema:
    decoded = decode_jwt(token)
    try:
        return TokenDataSchema.model_validate(decoded)
    except ValidationError:
        raise UnauthenticatedError


def create_access_token(schema: UserSchema) -> str:
    expire_timedelta = timedelta(minutes=settings.ACCESS_EXPIRE_MINUTER)
    return create_jwt_token(schema, TokenType.access, expire_timedelta)


def create_refresh_token(schema: UserSchema) -> str:
    expire_timedelta = timedelta(days=settings.REFRESH_EXPIRE_DAYS)
    return create_jwt_token(schema, TokenType.refresh, expire_timedelta)
