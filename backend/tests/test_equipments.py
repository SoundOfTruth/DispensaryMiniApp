import pytest
from httpx import AsyncClient

from src.models.equipments import Equipment, EquipmentType

pytestmark = pytest.mark.asyncio


class TestEquipmentApi:
    async def test_get_equipment_empty(self, client: AsyncClient):
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

    async def test_delete_equipment_unauth_(self, client: AsyncClient, equipment: Equipment):
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
