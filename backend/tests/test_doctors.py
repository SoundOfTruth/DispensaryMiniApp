import pytest
from httpx import AsyncClient

from src.models.doctors import Doctor
from src.schemas.doctors import DoctorSchema, SimpleDoctorSchema
from tests.utils import validate_pagination, validate_response_schema

pytestmark = pytest.mark.asyncio


class TestDoctorApi:
    payload_422 = [
        {"inspections": "", "education": "", "extra_education": ""},
        {"inspections": [""], "education": [""], "extra_education": {""}},
        {"inspections": ["qwe"], "education": ["Test"], "extra_education": ["Test"]},
        {"inspections": ["qwe"], "education": "Test", "extra_education": "Test"},
    ]

    async def test_get_doctors_empty(self, client: AsyncClient):
        response = await client.get("/api/doctors/")
        assert response.status_code == 200

    async def test_doctor_notfound(self, client: AsyncClient):
        response = await client.get("/api/doctors/9999/")
        assert response.status_code == 404

    async def test_get_doctor(self, client: AsyncClient, doctor: Doctor):
        response = await client.get(f"/api/doctors/{doctor.id}/")
        data = response.json()
        assert response.status_code == 200
        validate_response_schema(data, DoctorSchema)
        assert data.get("id") == doctor.id

    @pytest.mark.parametrize(
        "params",
        [
            {"limit": 2, "offset": 0},
            {"limit": 10, "offset": 10},
            {"limit": 20, "offset": 20},
            {"limit": 50, "offset": 0},
        ],
    )
    async def test_get_doctors_pagination(
        self, client: AsyncClient, many_doctors: list[Doctor], params: dict[str, int]
    ):
        response = await client.get("/api/doctors/", params=params)
        data = response.json()
        assert validate_pagination(
            data,
            SimpleDoctorSchema,
            len(many_doctors),
            limit=params["limit"],
            offset=params["offset"],
        )
