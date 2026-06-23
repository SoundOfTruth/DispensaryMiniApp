import pytest
from httpx import AsyncClient

from src.models.equipments import Equipment, EquipmentType
from src.schemas.equipments import EquipmentTypeSchema
from tests.utils import validate_response_schema

pytestmark = pytest.mark.asyncio


class Testequipment_typeApi:
    async def test_get_equipment_types_empty(self, client: AsyncClient):
        response = await client.get("/api/equipment-types/")
        assert response.status_code == 200

    async def test_get_equipment_types_unauth(
        self, client: AsyncClient, equipment_types
    ):
        response = await client.get("/api/equipment-types/")
        data = response.json()
        assert response.status_code == 200
        assert len(data) >= len(equipment_types)
        validate_response_schema(data, schema=EquipmentTypeSchema, many=True)

    async def test_get_equipment_types_user_role(
        self, user_client: AsyncClient, equipment_types
    ):
        response = await user_client.get("/api/equipment-types/")
        data = response.json()
        assert response.status_code == 200
        assert len(data) >= len(equipment_types)
        validate_response_schema(data, schema=EquipmentTypeSchema, many=True)

    async def test_get_equipment_types_admin_role(
        self, admin_client: AsyncClient, equipment_types
    ):
        response = await admin_client.get("/api/equipment-types/")
        data = response.json()
        assert response.status_code == 200
        assert len(data) >= len(equipment_types)
        validate_response_schema(data, schema=EquipmentTypeSchema, many=True)

    async def test_get_equipment_types_superuser_role(
        self, superuser_client: AsyncClient, equipment_types
    ):
        response = await superuser_client.get("/api/equipment-types/")
        data = response.json()
        assert response.status_code == 200
        assert len(data) >= len(equipment_types)
        validate_response_schema(data, schema=EquipmentTypeSchema, many=True)

    async def test_get_equipment_type_unauth(
        self, client: AsyncClient, equipment_type: EquipmentType
    ):
        response = await client.get(f"/api/equipment-types/{equipment_type.id}/")
        data = response.json()
        assert response.status_code == 200
        validate_response_schema(data, schema=EquipmentTypeSchema, many=True)

    async def test_get_equipment_type_user_role(
        self, user_client: AsyncClient, equipment_type: EquipmentType
    ):
        response = await user_client.get(f"/api/equipment-types/{equipment_type.id}/")
        data = response.json()
        assert response.status_code == 200
        validate_response_schema(data, schema=EquipmentTypeSchema, many=True)

    async def test_get_equipment_type_admin_role(
        self, admin_client: AsyncClient, equipment_type: EquipmentType
    ):
        response = await admin_client.get(f"/api/equipment-types/{equipment_type.id}/")
        data = response.json()
        assert response.status_code == 200
        validate_response_schema(data, schema=EquipmentTypeSchema, many=True)

    async def test_get_equipment_type_superuser_role(
        self, superuser_client: AsyncClient, equipment_type: EquipmentType
    ):
        response = await superuser_client.get(
            f"/api/equipment-types/{equipment_type.id}/"
        )
        data = response.json()
        assert response.status_code == 200
        validate_response_schema(data, schema=EquipmentTypeSchema, many=True)

    async def test_create_equipment_type_unauth(
        self, client: AsyncClient, gen_equipment_type_payload
    ):
        payload = gen_equipment_type_payload()
        response = await client.post("/api/equipment-types/", json=payload)
        assert response.status_code == 401

    async def test_create_equipment_type_user_role(
        self, user_client: AsyncClient, gen_equipment_type_payload
    ):
        payload = gen_equipment_type_payload()
        response = await user_client.post("/api/equipment-types/", json=payload)
        assert response.status_code == 403

    async def test_create_equipment_type_admin_role(
        self, admin_client: AsyncClient, gen_equipment_type_payload
    ):
        payload = gen_equipment_type_payload()
        response = await admin_client.post("/api/equipment-types/", json=payload)
        assert response.status_code == 201

    async def test_create_equipment_type_superuser_role(
        self, superuser_client: AsyncClient, gen_equipment_type_payload
    ):
        payload = gen_equipment_type_payload()
        response = await superuser_client.post("/api/equipment-types/", json=payload)
        assert response.status_code == 201

    async def test_create_equipment_type_empty_json(
        self, superuser_client: AsyncClient
    ):
        response = await superuser_client.post("/api/equipment-types/", json={})
        assert response.status_code == 422

    async def test_create_department_invalid_payload(
        self, superuser_client: AsyncClient
    ):
        payload = {"name": ""}
        response = await superuser_client.post("/api/equipment-types/", json=payload)
        assert response.status_code == 422

    async def test_update_equipment_type_empty_json(
        self, superuser_client: AsyncClient, equipment_type: EquipmentType
    ):
        response = await superuser_client.put(
            f"/api/equipment-types/{equipment_type.id}/", json={}
        )
        assert response.status_code == 422

    async def test_update_equipment_type_superuser_role(
        self,
        superuser_client: AsyncClient,
        equipment_type: EquipmentType,
        gen_equipment_type_payload,
    ):
        payload = gen_equipment_type_payload()
        response = await superuser_client.put(
            f"/api/equipment-types/{equipment_type.id}/", json=payload
        )
        assert response.status_code == 200

    async def test_update_equipment_type_admin_role(
        self,
        admin_client: AsyncClient,
        equipment_type: EquipmentType,
        gen_equipment_type_payload,
    ):
        payload = gen_equipment_type_payload()
        response = await admin_client.put(
            f"/api/equipment-types/{equipment_type.id}/", json=payload
        )
        assert response.status_code == 200

    async def test_update_equipment_type_user_role(
        self,
        user_client: AsyncClient,
        equipment_type: EquipmentType,
        gen_equipment_type_payload,
    ):
        payload = gen_equipment_type_payload()
        response = await user_client.put(
            f"/api/equipment-types/{equipment_type.id}/", json=payload
        )
        assert response.status_code == 403

    async def test_update_equipment_type_ivalid_payload(
        self,
        superuser_client: AsyncClient,
        equipment_type: EquipmentType,
    ):
        payload = {"name": ""}
        response = await superuser_client.put(
            f"/api/equipment-types/{equipment_type.id}/", json=payload
        )
        assert response.status_code == 422

    async def test_delete_equipment_type_superuser_role(
        self, superuser_client: AsyncClient, equipment_type: EquipmentType
    ):
        response = await superuser_client.delete(
            f"/api/equipment-types/{equipment_type.id}/"
        )
        assert response.status_code == 204

    async def test_delete_equipment_type_admin_role(
        self, admin_client: AsyncClient, equipment_type: EquipmentType
    ):
        response = await admin_client.delete(
            f"/api/equipment-types/{equipment_type.id}/"
        )
        assert response.status_code == 204

    async def test_delete_equipment_type_user_role(
        self, user_client: AsyncClient, equipment_type: EquipmentType
    ):
        response = await user_client.delete(
            f"/api/equipment-types/{equipment_type.id}/"
        )
        assert response.status_code == 403

    async def test_delete_related_equipment_type(
        self, superuser_client: AsyncClient, equipment: Equipment
    ):
        response = await superuser_client.delete(
            f"/api/equipment-types/{equipment.type_id}/"
        )
        assert response.status_code == 400
