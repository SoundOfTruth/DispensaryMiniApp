from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.api.exceptions import PermissionError
from src.models.users import Role
from src.schemas.auth import TokenDataSchema, TokenType
from src.services.exceptions import UnauthenticatedError
from src.utils.auth import get_token_data

security = HTTPBearer()

TokenDep = Annotated[HTTPAuthorizationCredentials, Depends(security)]


def get_access_data(token: TokenDep) -> TokenDataSchema:
    token_data = get_token_data(token.credentials)
    if token_data.type != TokenType.access.value:
        raise UnauthenticatedError
    return token_data


def has_superuser_permissions(token: TokenDep) -> TokenDataSchema:
    token_data = get_access_data(token)
    if token_data.role != Role.SUPERUSER.value:
        raise PermissionError
    return token_data


def has_admin_permissions(token: TokenDep) -> TokenDataSchema:
    token_data = get_access_data(token)
    if token_data.role != Role.ADMIN.value and token_data.role != Role.SUPERUSER.value:
        raise PermissionError
    return token_data


AccessTokenDep = Annotated[TokenDataSchema, Depends(get_access_data)]
AdminTokenDep = Annotated[TokenDataSchema, Depends(has_admin_permissions)]
SuperuserTokenDep = Annotated[TokenDataSchema, Depends(has_superuser_permissions)]
