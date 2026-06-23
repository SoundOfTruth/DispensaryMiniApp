import pytest
from httpx import AsyncClient

from src.models.doctors import Doctor, Speciality
from src.schemas.specialities import SpecialitySchema
from tests.utils import validate_response_schema

pytestmark = pytest.mark.asyncio


class TestSpecailityApi:
    async def test_get_specialties_empty(self, client: AsyncClient):
        response = await client.get("/api/specialties/")
        assert response.status_code == 200

    async def test_get_specialties_unauth(self, client: AsyncClient, specialties):
        response = await client.get("/api/specialties/")
        data = response.json()
        assert response.status_code == 200
        assert len(data) >= len(specialties)
        validate_response_schema(data, schema=SpecialitySchema, many=True)

    async def test_get_specialties_user_role(
        self, user_client: AsyncClient, specialties
    ):
        response = await user_client.get("/api/specialties/")
        data = response.json()
        assert response.status_code == 200
        assert len(data) >= len(specialties)
        validate_response_schema(data, schema=SpecialitySchema, many=True)

    async def test_get_specialties_admin_role(
        self, admin_client: AsyncClient, specialties
    ):
        response = await admin_client.get("/api/specialties/")
        data = response.json()
        assert response.status_code == 200
        assert len(data) >= len(specialties)
        validate_response_schema(data, schema=SpecialitySchema, many=True)

    async def test_get_specialties_superuser_role(
        self, superuser_client: AsyncClient, specialties
    ):
        response = await superuser_client.get("/api/specialties/")
        data = response.json()
        assert response.status_code == 200
        assert len(data) >= len(specialties)
        validate_response_schema(data, schema=SpecialitySchema, many=True)

    async def test_get_speciality_unauth(
        self, client: AsyncClient, speciality: Speciality
    ):
        response = await client.get(f"/api/specialties/{speciality.id}/")
        data = response.json()
        assert response.status_code == 200
        validate_response_schema(data, schema=SpecialitySchema, many=True)

    async def test_get_speciality_user_role(
        self, user_client: AsyncClient, speciality: Speciality
    ):
        response = await user_client.get(f"/api/specialties/{speciality.id}/")
        data = response.json()
        assert response.status_code == 200
        validate_response_schema(data, schema=SpecialitySchema, many=True)

    async def test_get_speciality_admin_role(
        self, admin_client: AsyncClient, speciality: Speciality
    ):
        response = await admin_client.get(f"/api/specialties/{speciality.id}/")
        data = response.json()
        assert response.status_code == 200
        validate_response_schema(data, schema=SpecialitySchema, many=True)

    async def test_get_speciality_superuser_role(
        self, superuser_client: AsyncClient, speciality: Speciality
    ):
        response = await superuser_client.get(f"/api/specialties/{speciality.id}/")
        data = response.json()
        assert response.status_code == 200
        validate_response_schema(data, schema=SpecialitySchema, many=True)

    async def test_create_specialty_unauth(
        self, client: AsyncClient, gen_speciality_payload
    ):
        payload = gen_speciality_payload()
        response = await client.post("/api/specialties/", json=payload)
        assert response.status_code == 401

    async def test_create_specialty_user_role(
        self, user_client: AsyncClient, gen_speciality_payload
    ):
        payload = gen_speciality_payload()
        response = await user_client.post("/api/specialties/", json=payload)
        assert response.status_code == 403

    async def test_create_specialty_admin_role(
        self, admin_client: AsyncClient, gen_speciality_payload
    ):
        payload = gen_speciality_payload()
        response = await admin_client.post("/api/specialties/", json=payload)
        assert response.status_code == 201

    async def test_create_specialty_superuser_role(
        self, superuser_client: AsyncClient, gen_speciality_payload
    ):
        payload = gen_speciality_payload()
        response = await superuser_client.post("/api/specialties/", json=payload)
        assert response.status_code == 201

    async def test_create_specialty_empty_json(self, superuser_client: AsyncClient):
        response = await superuser_client.post("/api/specialties/", json={})
        assert response.status_code == 422

    async def test_create_specialty_invalid_payload(
        self, superuser_client: AsyncClient
    ):
        payload = {"name": ""}
        response = await superuser_client.post("/api/specialties/", json=payload)
        assert response.status_code == 422

    async def test_update_specialty_superuser_role(
        self,
        superuser_client: AsyncClient,
        speciality: Speciality,
        gen_speciality_payload,
    ):
        payload = gen_speciality_payload()
        response = await superuser_client.put(
            f"/api/specialties/{speciality.id}/", json=payload
        )
        assert response.status_code == 200

    async def test_update_specialty_admin_role(
        self, admin_client: AsyncClient, speciality: Speciality, gen_speciality_payload
    ):
        payload = gen_speciality_payload()
        response = await admin_client.put(
            f"/api/specialties/{speciality.id}/", json=payload
        )
        assert response.status_code == 200

    async def test_update_specialty_user_role(
        self, user_client: AsyncClient, speciality: Speciality, gen_speciality_payload
    ):
        payload = gen_speciality_payload()
        response = await user_client.put(
            f"/api/specialties/{speciality.id}/", json=payload
        )
        assert response.status_code == 403

    async def test_update_specialty_empty_json(
        self, superuser_client: AsyncClient, speciality: Speciality
    ):
        response = await superuser_client.put(
            f"/api/specialties/{speciality.id}/", json={}
        )
        assert response.status_code == 422

    async def test_update_specialty_ivalid_payload(
        self, superuser_client: AsyncClient, speciality: Speciality
    ):
        payload = {"name": ""}
        response = await superuser_client.put(
            f"/api/specialties/{speciality.id}/", json=payload
        )
        assert response.status_code == 422

    async def test_delete_specialty_superuser_role(
        self, superuser_client: AsyncClient, speciality: Speciality
    ):
        response = await superuser_client.delete(f"/api/specialties/{speciality.id}/")
        assert response.status_code == 204

    async def test_delete_specialty_admin_role(
        self, admin_client: AsyncClient, speciality: Speciality
    ):
        response = await admin_client.delete(f"/api/specialties/{speciality.id}/")
        assert response.status_code == 204

    async def test_delete_specialty_user_role(
        self, user_client: AsyncClient, speciality: Speciality
    ):
        response = await user_client.delete(f"/api/specialties/{speciality.id}/")
        assert response.status_code == 403

    async def test_delete_related_speciality(
        self, superuser_client: AsyncClient, doctor: Doctor
    ):
        response = await superuser_client.delete(
            f"/api/specialties/{doctor.speciality_id}/"
        )
        assert response.status_code == 400
