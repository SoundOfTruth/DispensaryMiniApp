import pytest
from httpx import AsyncClient

from src.models.users import User

pytestmark = pytest.mark.asyncio


class TestAuthApi:
    async def test_login(self, client: AsyncClient, superuser: User, password):
        payload = {"email": superuser.email, "password": password}
        response = await client.post("/api/auth/login/", json=payload)
        data = response.json()
        assert response.status_code == 200
        assert data["access_token"]
        assert response.cookies.get("app_rt")
        assert not data.get("refresh_token")
        assert not data.get("app_rt")

    async def test_login_invalid_email(self, client: AsyncClient, password):
        payload = {"email": "invalid@email.com", "password": password}
        response = await client.post("/api/auth/login/", json=payload)
        assert response.status_code == 400

    async def test_login_invalid_password(self, client: AsyncClient, user: User):
        payload = {"email": user.email, "password": "invalidpassword"}
        response = await client.post("/api/auth/login/", json=payload)
        assert response.status_code == 400

    async def test_refresh_unauth(self, client: AsyncClient):
        response = await client.post("/api/auth/refresh/")
        assert response.status_code == 401

    async def test_refresh_no_cookies(self, superuser_client: AsyncClient):
        response = await superuser_client.post("/api/auth/refresh/")
        assert response.status_code == 401

    async def test_refresh_ivalid_token(self, client: AsyncClient):
        client.cookies = {"app_rt": "invalid"}
        response = await client.post("/api/auth/refresh/")
        assert response.status_code == 401

    async def test_refresh_superuser(
        self, client: AsyncClient, superuser_refresh_token
    ):
        client.cookies = {"app_rt": f"{superuser_refresh_token}"}
        response = await client.post("/api/auth/refresh/")
        data = response.json()
        assert response.status_code == 200
        assert data["access_token"]
        assert not response.cookies.get("app_rt")
        assert not data.get("refresh_token")
        assert not data.get("app_rt")

    async def test_refresh_admin(self, client: AsyncClient, admin_refresh_token):
        client.cookies = {"app_rt": f"{admin_refresh_token}"}
        response = await client.post("/api/auth/refresh/")
        data = response.json()
        assert response.status_code == 200
        assert data["access_token"]
        assert not response.cookies.get("app_rt")
        assert not data.get("refresh_token")
        assert not data.get("app_rt")

    async def test_refresh_user(self, client: AsyncClient, user_refresh_token):
        client.cookies = {"app_rt": f"{user_refresh_token}"}
        response = await client.post("/api/auth/refresh/")
        data = response.json()
        assert response.status_code == 200
        assert data["access_token"]
        assert not response.cookies.get("app_rt")
        assert not data.get("refresh_token")
        assert not data.get("app_rt")

    async def test_refresh_by_user_access_token(
        self, client: AsyncClient, user_access_token
    ):
        client.cookies = {"app_rt": f"{user_access_token}"}
        response = await client.post("/api/auth/refresh/")
        assert response.status_code == 401

    async def test_refresh_by_admin_access_token(
        self, client: AsyncClient, admin_access_token
    ):
        client.cookies = {"app_rt": f"{admin_access_token}"}
        response = await client.post("/api/auth/refresh/")
        assert response.status_code == 401

    async def test_refresh_by_superuser_access_token(
        self, client: AsyncClient, superuser_access_token
    ):
        client.cookies = {"app_rt": f"{superuser_access_token}"}
        response = await client.post("/api/auth/refresh/")
        assert response.status_code == 401
