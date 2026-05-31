import pytest
from httpx import AsyncClient

from src.models.doctors import Department, Doctor
from src.schemas.departments import DepartmentSchema
from tests.utils import validate_response_schema

pytestmark = pytest.mark.asyncio


class TestDepartmentApi:
    async def test_get_departments_empty(self, client: AsyncClient):
        response = await client.get("/api/departments/")
        assert response.status_code == 200

    async def test_get_departments(self, client: AsyncClient, departments):
        response = await client.get("/api/departments/")
        data = response.json()
        assert response.status_code == 200
        assert len(data) >= len(departments)
        validate_response_schema(data, schema=DepartmentSchema, many=True)

    async def test_get_department(self, client: AsyncClient, department: Department):
        response = await client.get(f"/api/departments/{department.id}/")
        data = response.json()
        assert response.status_code == 200
        validate_response_schema(data, schema=DepartmentSchema, many=True)

    async def test_get_department_user_role(
        self, user_client: AsyncClient, department: Department
    ):
        response = await user_client.get(f"/api/departments/{department.id}/")
        data = response.json()
        assert response.status_code == 200
        validate_response_schema(data, schema=DepartmentSchema, many=True)

    async def test_get_department_admin_role(
        self, admin_client: AsyncClient, department: Department
    ):
        response = await admin_client.get(f"/api/departments/{department.id}/")
        data = response.json()
        assert response.status_code == 200
        validate_response_schema(data, schema=DepartmentSchema, many=True)

    async def test_get_department_superuser_role(
        self, superuser_client: AsyncClient, department: Department
    ):
        response = await superuser_client.get(f"/api/departments/{department.id}/")
        data = response.json()
        assert response.status_code == 200
        validate_response_schema(data, schema=DepartmentSchema, many=True)

    @pytest.mark.usefixtures("departments")
    async def test_get_departments_user_role(self, user_client: AsyncClient):
        response = await user_client.get("/api/departments/")
        data = response.json()
        assert response.status_code == 200
        assert len(data) != 0

    @pytest.mark.usefixtures("departments")
    async def test_get_departments_admin_role(self, admin_client: AsyncClient):
        response = await admin_client.get("/api/departments/")
        data = response.json()
        assert response.status_code == 200
        assert len(data) != 0

    @pytest.mark.usefixtures("departments")
    async def test_get_departments_superuser_role(self, superuser_client: AsyncClient):
        response = await superuser_client.get("/api/departments/")
        data = response.json()
        assert response.status_code == 200
        assert len(data) != 0

    async def test_create_department_unauth(
        self, client: AsyncClient, gen_department_payload
    ):
        payload = gen_department_payload()
        response = await client.post("/api/departments/", json=payload)
        assert response.status_code == 401

    async def test_create_department_user_role(
        self, user_client: AsyncClient, gen_department_payload
    ):
        payload = gen_department_payload()
        response = await user_client.post("/api/departments/", json=payload)
        assert response.status_code == 403

    async def test_create_department_admin_role(
        self, admin_client: AsyncClient, gen_department_payload
    ):
        payload = gen_department_payload()
        response = await admin_client.post("/api/departments/", json=payload)
        assert response.status_code == 201

    async def test_create_department_superuser_role(
        self, superuser_client: AsyncClient, gen_department_payload
    ):
        payload = gen_department_payload()
        response = await superuser_client.post("/api/departments/", json=payload)
        assert response.status_code == 201

    async def test_create_department_empty_json(self, superuser_client: AsyncClient):
        response = await superuser_client.post("/api/departments/", json={})
        assert response.status_code == 422

    async def test_update_department_empty_json(
        self, superuser_client: AsyncClient, department: Department
    ):
        response = await superuser_client.put(
            f"/api/departments/{department.id}/", json={}
        )
        assert response.status_code == 422

    async def test_update_department_superuser_role(
        self, superuser_client: AsyncClient, department: Department, gen_department_payload
    ):
        payload = gen_department_payload()
        response = await superuser_client.put(
            f"/api/departments/{department.id}/", json=payload
        )
        assert response.status_code == 200

    async def test_update_department_admin_role(
        self, admin_client: AsyncClient, department: Department, gen_department_payload
    ):
        payload = gen_department_payload()
        response = await admin_client.put(
            f"/api/departments/{department.id}/", json=payload
        )
        assert response.status_code == 200

    async def test_update_department_user_role(
        self, user_client: AsyncClient, department: Department, gen_department_payload
    ):
        payload = gen_department_payload()
        response = await user_client.put(
            f"/api/departments/{department.id}/", json=payload
        )
        assert response.status_code == 403

    async def test_delete_department_superuser_role(
        self, superuser_client: AsyncClient, department: Department
    ):
        response = await superuser_client.delete(f"/api/departments/{department.id}/")
        assert response.status_code == 204

    async def test_delete_department_admin_role(
        self, admin_client: AsyncClient, department: Department
    ):
        response = await admin_client.delete(f"/api/departments/{department.id}/")
        assert response.status_code == 204

    async def test_delete_department_user_role(
        self, user_client: AsyncClient, department: Department
    ):
        response = await user_client.delete(f"/api/departments/{department.id}/")
        assert response.status_code == 403

    async def test_delete_related_Department(
        self, superuser_client: AsyncClient, doctor: Doctor
    ):
        response = await superuser_client.delete(
            f"/api/departments/{doctor.department_id}/"
        )
        assert response.status_code == 400
