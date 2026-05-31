import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestUploadApi:
    async def test_upload_file(self, superuser_client: AsyncClient, image):
        files = {"file": ("example.jpeg", image, "image/jpeg")}
        response = await superuser_client.post("/api/upload/", files=files)
        assert response.status_code == 201

    async def test_upload_file_unauth(self, client: AsyncClient, image):
        files = {"file": ("example.jpeg", image, "image/jpeg")}
        response = await client.post("/api/upload/", files=files)
        assert response.status_code == 401

    async def test_upload_file_user_role(self, user_client: AsyncClient, image):
        files = {"file": ("example.jpeg", image, "image/jpeg")}
        response = await user_client.post("/api/upload/", files=files)
        assert response.status_code == 403

    async def test_upload_file_admin_role(self, admin_client: AsyncClient, image):
        files = {"file": ("example.jpeg", image, "image/jpeg")}
        response = await admin_client.post("/api/upload/", files=files)
        assert response.status_code == 201
