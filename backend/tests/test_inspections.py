import pytest
from httpx import AsyncClient

from src.models.doctors import Doctor
from src.models.inspections import Inspection
from src.schemas.inspections import InspectionSchema, SimpleInspectionSchema
from tests.utils import FakerSingleton, validate_pagination, validate_response_schema

faker = FakerSingleton()

pytestmark = pytest.mark.asyncio

payload = {
    "title": "test",
    "description": "test",
    "preparation": "test",
    "doctors": [],
}


def gen_invalid_payload():
    yield {}
    yield []
    yield None
    yield ""
    fields = ["title", "doctors"]
    for field in fields:
        new_payload = payload.copy()
        new_payload["title"] = faker.unique.name()
        new_payload[field] = ""
        yield new_payload


def gen_invalid_create_payload():
    for data in gen_invalid_payload():
        yield data
    fields = payload.keys()
    for field in fields:
        new_payload = payload.copy()
        new_payload["title"] = faker.unique.name()
        new_payload.pop(field, None)
        yield new_payload


class TestInspectionApi:
    patch_payload = [
        {"title": faker.unique.name()},
        {"description": ""},
        {"preparation": ""},
        {"doctors": []},
        {
            "title": faker.unique.name(),
            "description": "",
            "preparation": "",
        },
        {
            "title": faker.unique.name(),
            "description": "",
            "preparation": "",
            "doctors": [],
        },
    ]

    async def test_get_inspections_empty(self, client: AsyncClient):
        response = await client.get("/api/inspections/")
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "params",
        [
            {"limit": 2, "offset": 0},
            {"limit": 10, "offset": 10},
            {"limit": 20, "offset": 20},
            {"limit": 50, "offset": 0},
        ],
    )
    async def test_inspections_pagination(
        self,
        client: AsyncClient,
        many_inspections: list[Inspection],
        params: dict[str, int],
    ):
        response = await client.get("/api/inspections/", params=params)
        data = response.json()
        assert validate_pagination(
            data=data,
            schema=SimpleInspectionSchema,
            fixture_length=len(many_inspections),
            limit=params["limit"],
            offset=params["offset"],
        )

    @pytest.mark.usefixtures("inspections")
    async def test_get_inspections_user_role(self, user_client: AsyncClient):
        response = await user_client.get("/api/inspections/")
        assert response.status_code == 200

    @pytest.mark.usefixtures("inspections")
    async def test_get_inspections_admin_role(self, admin_client: AsyncClient):
        response = await admin_client.get("/api/inspections/")
        assert response.status_code == 200

    @pytest.mark.usefixtures("inspections")
    async def test_get_inspections_superuser_role(self, superuser_client: AsyncClient):
        response = await superuser_client.get("/api/inspections/")
        assert response.status_code == 200

    async def get_inspection_notfound(self, client: AsyncClient):
        response = await client.get("/api/inspections/9999/")
        assert response.status_code == 404

    async def test_get_inspecton_unauth(
        self, client: AsyncClient, inspection: Inspection
    ):
        response = await client.get(f"/api/inspections/{inspection.id}/")
        assert response.status_code == 200
        assert validate_response_schema(response.json(), InspectionSchema)

    async def test_get_inspecton_user_role(
        self, user_client: AsyncClient, inspection: Inspection
    ):
        response = await user_client.get(f"/api/inspections/{inspection.id}/")
        assert response.status_code == 200
        assert validate_response_schema(response.json(), InspectionSchema)

    async def test_get_inspecton_admin_role(
        self, admin_client: AsyncClient, inspection: Inspection
    ):
        response = await admin_client.get(f"/api/inspections/{inspection.id}/")
        assert response.status_code == 200
        assert validate_response_schema(response.json(), InspectionSchema)

    async def test_get_inspecton_superuser_role(
        self, superuser_client: AsyncClient, inspection: Inspection
    ):
        response = await superuser_client.get(f"/api/inspections/{inspection.id}/")
        assert response.status_code == 200
        assert validate_response_schema(response.json(), InspectionSchema)

    async def test_create_inspection_unauth(self, client: AsyncClient):
        response = await client.post("/api/inspections/", json={"name": "Test"})
        assert response.status_code == 401

    async def test_create_inspection_user_role(
        self, user_client: AsyncClient, gen_inspection_payload
    ):
        payload = gen_inspection_payload()
        response = await user_client.post("/api/inspections/", json=payload)
        assert response.status_code == 403

    async def test_create_inspection_admin_role(
        self, admin_client: AsyncClient, gen_inspection_payload
    ):
        payload = gen_inspection_payload()
        response = await admin_client.post("/api/inspections/", json=payload)
        assert response.status_code == 201

    async def test_create_inspection_with_doctors(
        self,
        superuser_client: AsyncClient,
        gen_inspection_payload,
        doctors: list[Doctor],
    ):
        payload = gen_inspection_payload()
        payload["doctors"] = [{"id": doctor.id} for doctor in doctors]
        response = await superuser_client.post("/api/inspections/", json=payload)
        data = response.json()
        assert response.status_code == 201
        assert len(data["doctors"]) == len(doctors)

    async def test_create_inspection_existing_title(
        self,
        superuser_client: AsyncClient,
        gen_inspection_payload,
        inspection: Inspection,
    ):
        payload = gen_inspection_payload()
        payload["title"] = inspection.title
        response = await superuser_client.post("/api/inspections/", json=payload)
        assert response.status_code == 400

    async def test_create_inspection_with_unexist_doctors(
        self, superuser_client: AsyncClient, gen_inspection_payload, doctor: Doctor
    ):
        payload = gen_inspection_payload()
        payload["doctors"] = [{"id": doctor.id}, {"id": 9999}]
        response = await superuser_client.post("/api/inspections/", json=payload)
        assert response.status_code == 400

    @pytest.mark.parametrize("payload", list(gen_invalid_create_payload()))
    async def test_create_inspection_incorrect_payload(
        self, superuser_client: AsyncClient, payload
    ):
        response = await superuser_client.post("/api/inspections/", json=payload)
        assert response.status_code == 422

    async def test_update_inspection_unauth(
        self, client: AsyncClient, inspection: Inspection, gen_inspection_payload
    ):
        payload = gen_inspection_payload()
        response = await client.patch(
            f"/api/inspections/{inspection.id}/", json=payload
        )
        assert response.status_code == 401

    async def test_update_inspection_user_role(
        self, user_client: AsyncClient, inspection: Inspection, gen_inspection_payload
    ):
        payload = gen_inspection_payload()
        response = await user_client.patch(
            f"/api/inspections/{inspection.id}/", json=payload
        )
        assert response.status_code == 403

    async def test_update_inspection_admin_role(
        self, admin_client: AsyncClient, inspection: Inspection, gen_inspection_payload
    ):
        payload = gen_inspection_payload()
        response = await admin_client.patch(
            f"/api/inspections/{inspection.id}/", json=payload
        )
        assert response.status_code == 200

    async def test_update_inspection_with_existing_title(
        self,
        superuser_client: AsyncClient,
        gen_inspection_payload,
        inspection: Inspection,
        other_inspection: Inspection,
    ):
        payload = gen_inspection_payload()
        payload["title"] = other_inspection.title
        response = await superuser_client.patch(
            f"/api/inspections/{inspection.id}/", json=payload
        )
        assert response.status_code == 400

    async def test_update_inspection_with_doctors(
        self,
        superuser_client: AsyncClient,
        inspection_with_doctors: Inspection,
        gen_inspection_payload,
        doctors: list[Doctor],
    ):
        payload = gen_inspection_payload()
        payload["doctors"] = [{"id": doctor.id} for doctor in doctors]
        response = await superuser_client.patch(
            f"/api/inspections/{inspection_with_doctors.id}/", json=payload
        )
        data = response.json()
        assert response.status_code == 200
        assert len(data["doctors"]) == len(doctors)

    async def test_update_inspection_with_unexist_doctors(
        self,
        superuser_client: AsyncClient,
        inspection: Inspection,
        gen_inspection_payload,
        doctor: Doctor,
    ):
        payload = gen_inspection_payload()
        payload["doctors"] = [{"id": doctor.id}, {"id": 9999}]
        response = await superuser_client.patch(
            f"/api/inspections/{inspection.id}/", json=payload
        )
        assert response.status_code == 400

    @pytest.mark.parametrize("payload", list(gen_invalid_payload()))
    async def test_update_inspection_incorrect_payload(
        self, admin_client: AsyncClient, inspection: Inspection, payload
    ):
        response = await admin_client.patch(
            f"/api/inspections/{inspection.id}/", json=payload
        )
        assert response.status_code in [400, 422]

    @pytest.mark.parametrize("payload", patch_payload)
    async def test_patch_inspections(
        self,
        superuser_client: AsyncClient,
        inspection_with_doctors: Inspection,
        payload,
    ):
        response = await superuser_client.patch(
            f"/api/inspections/{inspection_with_doctors.id}/", json=payload
        )
        data = response.json()
        assert response.status_code == 200
        assert validate_response_schema(data, schema=Inspection)
        for key in payload:
            assert data[key] == payload[key]

    async def test_delete_inspection_unauth(
        self, client: AsyncClient, inspection: Inspection
    ):
        response = await client.delete(f"/api/inspections/{inspection.id}/")
        assert response.status_code == 401

    async def test_delete_inspection_user_role(
        self, user_client: AsyncClient, inspection: Inspection
    ):
        response = await user_client.delete(f"/api/inspections/{inspection.id}/")
        assert response.status_code == 403

    async def test_delete_inspection_admin_role(
        self, admin_client: AsyncClient, inspection: Inspection
    ):
        response = await admin_client.delete(f"/api/inspections/{inspection.id}/")
        assert response.status_code == 204

    async def test_delete_inspection_superuser_role(
        self, superuser_client: AsyncClient, inspection: Inspection
    ):
        response = await superuser_client.delete(f"/api/inspections/{inspection.id}/")
        assert response.status_code == 204
