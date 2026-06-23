import pytest
from httpx import AsyncClient

from src.models.equipments import Equipment, EquipmentType
from src.schemas.equipments import SimpleEquipmentSchema
from tests.utils import FakerSingleton, other_image_link, validate_response_schema

faker = FakerSingleton()

pytestmark = pytest.mark.asyncio

payload = {
    "name": "test",
    "image": other_image_link,
}


def gen_invalid_payload():
    yield {}
    yield []
    yield None
    yield ""
    fields = payload.keys()
    for field in fields:
        new_payload = payload.copy()
        new_payload["name"] = faker.unique.name()
        new_payload[field] = ""
        yield new_payload


def gen_invalid_create_payload():
    for data in gen_invalid_payload():
        yield data
    fields = payload.keys()
    for field in fields:
        new_payload = payload.copy()
        new_payload["name"] = faker.unique.name()
        new_payload.pop(field, None)
        yield new_payload


class TestEquipmentApi:
    patch_payload = [
        {"name": faker.unique.name(), "image": other_image_link},
        {"name": faker.unique.name()},
        {"image": other_image_link},
    ]

    async def test_get_equipment_empty(self, client: AsyncClient):
        response = await client.get("/api/equipments/")
        assert response.status_code == 200

    @pytest.mark.usefixtures("equipments")
    async def test_get_equipments_unauth(self, client: AsyncClient):
        response = await client.get("/api/equipments/")
        assert response.status_code == 200

    @pytest.mark.usefixtures("equipments")
    async def test_get_equipments_user_role(self, user_client: AsyncClient):
        response = await user_client.get("/api/equipments/")
        assert response.status_code == 200

    @pytest.mark.usefixtures("equipments")
    async def test_get_equipments_admin_role(self, admin_client: AsyncClient):
        response = await admin_client.get("/api/equipments/")
        assert response.status_code == 200

    @pytest.mark.usefixtures("equipments")
    async def test_get_equipments_superuser_role(self, superuser_client: AsyncClient):
        response = await superuser_client.get("/api/equipments/")
        assert response.status_code == 200

    async def test_get_equipment_unauth(
        self, client: AsyncClient, equipment: Equipment
    ):
        response = await client.get(f"/api/equipments/{equipment.id}/")
        assert response.status_code == 200

    async def test_get_equipment_user_role(
        self, user_client: AsyncClient, equipment: Equipment
    ):
        response = await user_client.get(f"/api/equipments/{equipment.id}/")
        assert response.status_code == 200

    async def test_get_equipment_admin_role(
        self, admin_client: AsyncClient, equipment: Equipment
    ):
        response = await admin_client.get(f"/api/equipments/{equipment.id}/")
        assert response.status_code == 200

    async def test_get_equipment_superuser_role(
        self, superuser_client: AsyncClient, equipment: Equipment
    ):
        response = await superuser_client.get(f"/api/equipments/{equipment.id}/")
        assert response.status_code == 200

    async def test_create_equipment_unauth(
        self,
        client: AsyncClient,
        gen_equipment_payload,
        related_equipment_type: EquipmentType,
    ):
        payload = gen_equipment_payload(related_equipment_type.id)
        response = await client.post("/api/equipments/", json=payload)
        assert response.status_code == 401

    async def test_create_equipment_user_role(
        self,
        user_client: AsyncClient,
        gen_equipment_payload,
        related_equipment_type: EquipmentType,
    ):
        payload = gen_equipment_payload(related_equipment_type.id)
        response = await user_client.post("/api/equipments/", json=payload)
        assert response.status_code == 403

    async def test_create_equipment_admin_role(
        self,
        admin_client: AsyncClient,
        gen_equipment_payload,
        related_equipment_type: EquipmentType,
    ):
        payload = gen_equipment_payload(related_equipment_type.id)
        response = await admin_client.post("/api/equipments/", json=payload)
        assert response.status_code == 201

    async def test_create_equipment_superuser_role(
        self,
        superuser_client: AsyncClient,
        gen_equipment_payload,
        related_equipment_type: EquipmentType,
    ):
        payload = gen_equipment_payload(related_equipment_type.id)
        response = await superuser_client.post("/api/equipments/", json=payload)
        assert response.status_code == 201

    @pytest.mark.parametrize("image_link", ["string", "http://ivalid.com"])
    async def test_create_equipment_bad_image_url(
        self,
        superuser_client: AsyncClient,
        gen_equipment_payload,
        related_equipment_type: EquipmentType,
        image_link: str,
    ):
        payload = gen_equipment_payload(related_equipment_type.id)
        payload["image"] = image_link
        response = await superuser_client.post("/api/equipments/", json=payload)
        assert response.status_code == 422 or 400

    async def test_create_unexisting_equipment_type(
        self, superuser_client: AsyncClient, gen_equipment_payload
    ):
        payload = gen_equipment_payload(9999)
        response = await superuser_client.post("/api/equipments/", json=payload)
        assert response.status_code == 400

    async def test_create_existing_equipment_name(
        self,
        superuser_client: AsyncClient,
        gen_equipment_payload,
        equipment: Equipment,
        other_equipment: Equipment,
    ):
        payload = gen_equipment_payload(equipment.type_id)
        payload["name"] = other_equipment.name
        await superuser_client.post("/api/equipments/", json=payload)
        response = await superuser_client.post("/api/equipments/", json=payload)
        assert response.status_code == 400

    @pytest.mark.parametrize("payload", list(gen_invalid_create_payload()))
    async def test_create_equipment_invalid_payload(
        self,
        superuser_client: AsyncClient,
        related_equipment_type: EquipmentType,
        payload,
    ):
        if type(payload) is dict:
            payload["type_id"] = related_equipment_type.id
        response = await superuser_client.post("/api/equipments/", json=payload)
        assert response.status_code == 422

    async def test_update_equipment_unauth(
        self,
        client: AsyncClient,
        equipment: Equipment,
        gen_equipment_payload,
        related_equipment_type,
    ):
        payload = gen_equipment_payload(related_equipment_type.id)
        response = await client.patch(f"/api/equipments/{equipment.id}/", json=payload)
        assert response.status_code == 401

    async def test_update_equipment_user_role(
        self,
        user_client: AsyncClient,
        equipment: Equipment,
        gen_equipment_payload,
        related_equipment_type,
    ):
        payload = gen_equipment_payload(related_equipment_type.id)
        response = await user_client.patch(
            f"/api/equipments/{equipment.id}/", json=payload
        )
        assert response.status_code == 403

    async def test_update_equipment_admin_role(
        self,
        admin_client: AsyncClient,
        equipment: Equipment,
        gen_equipment_payload,
        related_equipment_type,
    ):
        payload = gen_equipment_payload(related_equipment_type.id)
        response = await admin_client.patch(
            f"/api/equipments/{equipment.id}/", json=payload
        )
        assert response.status_code == 200

    async def test_update_equipment_superuser_role(
        self,
        superuser_client: AsyncClient,
        equipment: Equipment,
        gen_equipment_payload,
        related_equipment_type,
    ):
        payload = gen_equipment_payload(related_equipment_type.id)
        response = await superuser_client.patch(
            f"/api/equipments/{equipment.id}/", json=payload
        )
        assert response.status_code == 200

    async def test_update_unexisting_equipment_type(
        self, superuser_client: AsyncClient, gen_equipment_payload
    ):
        payload = gen_equipment_payload(9999)
        response = await superuser_client.post("/api/equipments/", json=payload)
        assert response.status_code == 400

    async def test_update_existing_equipment_name(
        self,
        superuser_client: AsyncClient,
        gen_equipment_payload,
        equipment: Equipment,
        other_equipment: Equipment,
    ):
        payload = gen_equipment_payload(equipment.type_id)
        payload["name"] = other_equipment.name
        response = await superuser_client.patch(
            f"/api/equipments/{equipment.id}/", json=payload
        )
        assert response.status_code == 400

    @pytest.mark.parametrize("image_link", ["string", "http://ivalid.com"])
    async def test_update_equipment_bad_image_url(
        self,
        superuser_client: AsyncClient,
        gen_equipment_payload,
        equipment: Equipment,
        related_equipment_type: EquipmentType,
        image_link: str,
    ):
        payload = gen_equipment_payload(related_equipment_type.id)
        payload["image"] = image_link
        response = await superuser_client.patch(
            f"/api/equipments/{equipment.id}", json=payload
        )
        assert response.status_code == 422 or 400

    @pytest.mark.parametrize("payload", list(gen_invalid_payload()))
    async def test_update_equipment_invalid_payload(
        self,
        superuser_client: AsyncClient,
        equipment: Equipment,
        related_equipment_type: EquipmentType,
        payload,
    ):
        if payload and type(payload) is dict:
            payload["type_id"] = related_equipment_type.id
        response = await superuser_client.patch(
            f"/api/equipments/{equipment.id}/", json=payload
        )
        assert response.status_code == 422 or response.status_code == 400

    async def test_patch_equipment_with_type_id(
        self,
        superuser_client: AsyncClient,
        equipment: Equipment,
        other_equipment_type: EquipmentType,
    ):
        payload = {"type_id": other_equipment_type.id}
        response = await superuser_client.patch(
            f"/api/equipments/{equipment.id}/", json=payload
        )
        assert response.status_code == 200

    async def test_patch_equipment_unexists_type_id(
        self,
        superuser_client: AsyncClient,
        equipment: Equipment,
    ):
        payload = {"type_id": 9999}
        response = await superuser_client.patch(
            f"/api/equipments/{equipment.id}/", json=payload
        )
        assert response.status_code == 400

    @pytest.mark.parametrize("payload", patch_payload)
    async def test_patch_equipment(
        self, superuser_client: AsyncClient, equipment: Equipment, payload
    ):
        response = await superuser_client.patch(
            f"/api/equipments/{equipment.id}/", json=payload
        )
        data = response.json()
        assert response.status_code == 200
        assert validate_response_schema(data, schema=SimpleEquipmentSchema)
        for key in payload:
            assert data[key] == payload[key]

    async def test_delete_equipment_unauth_(
        self, client: AsyncClient, equipment: Equipment
    ):
        response = await client.delete(f"/api/equipments/{equipment.id}/")
        assert response.status_code == 401

    async def test_delete_equipment_user_role(
        self, user_client: AsyncClient, equipment: Equipment
    ):
        response = await user_client.delete(f"/api/equipments/{equipment.id}/")
        assert response.status_code == 403

    async def test_delete_equipment_admin_role(
        self, admin_client: AsyncClient, equipment: Equipment
    ):
        response = await admin_client.delete(f"/api/equipments/{equipment.id}/")
        assert response.status_code == 204

    async def test_delete_equipment_superuser_role(
        self, superuser_client: AsyncClient, equipment: Equipment
    ):
        response = await superuser_client.delete(f"/api/equipments/{equipment.id}/")
        assert response.status_code == 204
