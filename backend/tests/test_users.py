import pytest
from httpx import AsyncClient

from src.models.users import User
from src.schemas.users import UserSchema
from tests.utils import validate_pagination, validate_response_schema

pytestmark = pytest.mark.asyncio


class TestUsersApi:
    async def test_get_users_pagination(self, superuser_client: AsyncClient, users):
        limit = 2
        params = {"limit": limit, "offset": 0}
        response = await superuser_client.get("/api/users/", params=params)
        data = response.json()
        assert validate_pagination(
            data=data,
            schema=UserSchema,
            fixture_length=len(users),
            limit=params["limit"],
            offset=params["offset"],
        )

    async def test_get_users_default_pagination(self, admin_client: AsyncClient, users):
        response = await admin_client.get("/api/users/")
        data = response.json()
        assert validate_pagination(
            data=data,
            schema=UserSchema,
            fixture_length=len(users),
        )

    async def test_get_users_superuser_role(self, superuser_client: AsyncClient):
        response = await superuser_client.get("/api/users/")
        assert response.status_code == 200

    async def test_get_users_admin_role(self, admin_client: AsyncClient):
        response = await admin_client.get("/api/users/")
        assert response.status_code == 200

    async def test_get_users_user_role(self, user_client: AsyncClient):
        response = await user_client.get("/api/users/")
        assert response.status_code == 403

    async def test_get_users_unauth(self, client: AsyncClient):
        response = await client.get("/api/users/")
        assert response.status_code == 401

    async def test_get_user_superuser_role(
        self, superuser_client: AsyncClient, another_user
    ):
        response = await superuser_client.get(f"/api/users/{another_user.id}/")
        assert response.status_code == 200
        assert validate_response_schema(response.json(), UserSchema)

    async def test_get_user_admin_role(self, admin_client: AsyncClient, another_user):
        response = await admin_client.get(f"/api/users/{another_user.id}/")
        assert response.status_code == 200
        assert validate_response_schema(response.json(), UserSchema)

    async def test_get_user_user_role(self, user_client: AsyncClient, another_user):
        response = await user_client.get(f"/api/users/{another_user.id}/")
        assert response.status_code == 403

    async def test_get_user_unauth(self, client: AsyncClient, another_user):
        response = await client.get(f"/api/users/{another_user.id}/")
        assert response.status_code == 401

    async def test_get_user_not_found(self, admin_client: AsyncClient):
        response = await admin_client.get("/api/users/9999/")
        assert response.status_code == 404

    async def test_get_me_superuser_role(
        self, superuser_client: AsyncClient, superuser: User
    ):
        response = await superuser_client.get("/api/users/me/")
        data = response.json()
        assert response.status_code == 200
        assert data["id"] == superuser.id
        assert validate_response_schema(data, UserSchema)

    async def test_get_me_admin_role(self, admin_client: AsyncClient, admin: User):
        response = await admin_client.get("/api/users/me/")
        data = response.json()
        assert response.status_code == 200
        assert data["id"] == admin.id

    async def test_get_me_user_role(self, user_client: AsyncClient, user: User):
        response = await user_client.get("/api/users/me/")
        data = response.json()
        assert response.status_code == 200
        assert data["id"] == user.id

    async def test_get_me_unauth(self, client: AsyncClient):
        response = await client.get("/api/users/me/")
        assert response.status_code == 401
