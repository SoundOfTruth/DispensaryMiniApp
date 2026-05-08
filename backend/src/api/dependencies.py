from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

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


def get_admin_data(token: TokenDep) -> TokenDataSchema:
    token_data = get_access_data(token)
    if not token_data.is_admin:
        raise
    return token_data


AccessTokenDep = Annotated[TokenDataSchema, Depends(get_access_data)]
AdminTokenDep = Annotated[TokenDataSchema, Depends(get_admin_data)]
