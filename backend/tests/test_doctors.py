import pytest
from httpx import AsyncClient

from src.models.doctors import Department, Doctor, Speciality
from src.models.inspections import Inspection
from src.schemas.doctors import SimpleDoctorSchema, SimpleInspectionSchema
from tests.utils import (
    FakerSingleton,
    other_image_link,
    validate_pagination,
    validate_response_schema,
)

faker = FakerSingleton()


class DoctorSchema(SimpleDoctorSchema):
    experience_start: int | None
    experience_years: int | None

    education: list[str]
    extra_education: list[str]
    inspections: list[SimpleInspectionSchema]


payload = {
    "photo": None,
    "firstname": "test",
    "lastname": "test",
    "middlename": "test",
    "qualification": "test",
    "experience_start": 2000,
    "education": [],
    "extra_education": [],
    "inspections": [],
}


def gen_invalid_payload():
    yield {}
    yield []
    yield None
    yield ""
    fields = payload.keys()
    for field in fields:
        new_payload = payload.copy()
        new_payload[field] = ""
        yield new_payload
    new_payload = payload.copy()
    new_payload["photo"] = "http://invalid.com"
    yield new_payload


def gen_invalid_create_payload():
    for data in gen_invalid_payload():
        yield data
    fields = payload.keys()
    for field in fields:
        new_payload = payload.copy()
        new_payload.pop(field, None)
        yield new_payload


pytestmark = pytest.mark.asyncio


class TestDoctorApi:
    patch_payload = [
        {"photo": other_image_link},
        {"firstname": faker.first_name()},
        {"lastname": faker.last_name()},
        {"middlename": faker.last_name()},
        {"qualification": faker.name()},
        {"experience_start": faker.random_int(min=1921, max=2026)},
        {"education": ["test1", "test2", "test3"]},
        {"extra_education": ["test1", "test2", "test3"]},
        {
            "education": ["test1", "test2", "test3"],
            "extra_education": ["test1", "test2", "test3"],
        },
    ]

    async def test_get_doctors_empty(self, client: AsyncClient):
        response = await client.get("/api/doctors/")
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

    @pytest.mark.usefixtures("doctors")
    async def test_get_doctors_user_role(self, client: AsyncClient):
        response = await client.get("/api/doctors/")
        assert response.status_code == 200

    @pytest.mark.usefixtures("doctors")
    async def test_get_doctors_admin_role(self, admin_client: AsyncClient):
        response = await admin_client.get("/api/doctors/")
        assert response.status_code == 200

    @pytest.mark.usefixtures("doctors")
    async def test_get_doctors_superuser_role(self, superuser_client: AsyncClient):
        response = await superuser_client.get("/api/doctors/")
        assert response.status_code == 200

    async def test_get_doctor_notfound(self, client: AsyncClient):
        response = await client.get("/api/doctors/9999/")
        assert response.status_code == 404

    async def test_get_doctor_unauth(self, client: AsyncClient, doctor: Doctor):
        response = await client.get(f"/api/doctors/{doctor.id}/")
        data = response.json()
        assert response.status_code == 200
        validate_response_schema(data, DoctorSchema)
        assert data.get("id") == doctor.id

    async def test_get_doctor_user_role(self, user_client: AsyncClient, doctor: Doctor):
        response = await user_client.get(f"/api/doctors/{doctor.id}/")
        data = response.json()
        assert response.status_code == 200
        validate_response_schema(data, DoctorSchema)
        assert data.get("id") == doctor.id

    async def test_get_doctor_admin_role(
        self, admin_client: AsyncClient, doctor: Doctor
    ):
        response = await admin_client.get(f"/api/doctors/{doctor.id}/")
        data = response.json()
        assert response.status_code == 200
        validate_response_schema(data, DoctorSchema)
        assert data.get("id") == doctor.id

    async def test_get_doctor_superuser_role(
        self, superuser_client: AsyncClient, doctor: Doctor
    ):
        response = await superuser_client.get(f"/api/doctors/{doctor.id}/")
        data = response.json()
        assert response.status_code == 200
        validate_response_schema(data, DoctorSchema)
        assert data.get("id") == doctor.id

    async def test_create_doctor_unauth(
        self,
        client: AsyncClient,
        gen_doctor_payload,
        doctor_speciality: Speciality,
        doctor_department: Department,
    ):
        payload = gen_doctor_payload(doctor_speciality.id, doctor_department.id)
        response = await client.post("/api/doctors/", json=payload)
        assert response.status_code == 401

    async def test_create_doctor_user_role(
        self,
        user_client: AsyncClient,
        gen_doctor_payload,
        doctor_speciality: Speciality,
        doctor_department: Department,
    ):
        payload = gen_doctor_payload(doctor_speciality.id, doctor_department.id)
        response = await user_client.post("/api/doctors/", json=payload)
        assert response.status_code == 403

    async def test_create_doctor_admin_role(
        self,
        admin_client: AsyncClient,
        gen_doctor_payload,
        doctor_speciality: Speciality,
        doctor_department: Department,
    ):
        payload = gen_doctor_payload(doctor_speciality.id, doctor_department.id)
        response = await admin_client.post("/api/doctors/", json=payload)
        assert response.status_code == 201

    async def test_create_doctor_with_inspections(
        self,
        superuser_client: AsyncClient,
        gen_doctor_payload,
        doctor_speciality: Speciality,
        doctor_department: Department,
        inspections: list[Inspection],
    ):
        payload = gen_doctor_payload(doctor_speciality.id, doctor_department.id)
        payload["inspections"] = [{"id": inspection.id} for inspection in inspections]
        response = await superuser_client.post("/api/doctors/", json=payload)
        data = response.json()
        assert response.status_code == 201
        assert len(data["inspections"]) == len(inspections)

    async def test_create_doctor_with_unexsists_inspections(
        self,
        superuser_client: AsyncClient,
        gen_doctor_payload,
        doctor_speciality: Speciality,
        doctor_department: Department,
        inspection: Inspection,
    ):
        payload = gen_doctor_payload(doctor_speciality.id, doctor_department.id)
        payload["inspections"] = [{"id": inspection.id}, {"id": 9999}]
        response = await superuser_client.post("/api/doctors/", json=payload)
        assert response.status_code == 400

    async def test_create_doctor_with_unexsists_speciality(
        self,
        superuser_client: AsyncClient,
        gen_doctor_payload,
        doctor_department: Department,
    ):
        payload = gen_doctor_payload(9999, doctor_department.id)
        response = await superuser_client.post("/api/doctors/", json=payload)
        assert response.status_code == 400

    async def test_create_doctor_with_unexsists_department(
        self,
        superuser_client: AsyncClient,
        gen_doctor_payload,
        doctor_speciality: Speciality,
    ):
        payload = gen_doctor_payload(doctor_speciality.id, 9999)
        response = await superuser_client.post("/api/doctors/", json=payload)
        assert response.status_code == 400

    @pytest.mark.parametrize("payload", list(gen_invalid_create_payload()))
    async def test_create_doctor_invalid_payload(
        self,
        superuser_client: AsyncClient,
        payload,
        doctor_speciality: Speciality,
        doctor_department: Department,
    ):
        if payload and type(payload) is dict:
            payload["speciality_id"] = doctor_speciality.id
            payload["department_id"] = doctor_department.id
        response = await superuser_client.post("/api/doctors/", json=payload)
        assert response.status_code == 422 or response.status_code == 400

    async def test_update_doctor_unauth(
        self,
        client: AsyncClient,
        doctor: Doctor,
        gen_doctor_payload,
        doctor_speciality: Speciality,
        doctor_department: Department,
    ):
        payload = gen_doctor_payload(doctor_speciality.id, doctor_department.id)
        response = await client.patch(f"/api/doctors/{doctor.id}/", json=payload)
        assert response.status_code == 401

    async def test_update_doctor_user_role(
        self,
        user_client: AsyncClient,
        doctor: Doctor,
        gen_doctor_payload,
        doctor_speciality: Speciality,
        doctor_department: Department,
    ):
        payload = gen_doctor_payload(doctor_speciality.id, doctor_department.id)
        response = await user_client.patch(f"/api/doctors/{doctor.id}/", json=payload)
        assert response.status_code == 403

    async def test_update_doctor_admin_role(
        self,
        admin_client: AsyncClient,
        doctor: Doctor,
        gen_doctor_payload,
        doctor_speciality: Speciality,
        doctor_department: Department,
    ):
        payload = gen_doctor_payload(doctor_speciality.id, doctor_department.id)
        response = await admin_client.patch(f"/api/doctors/{doctor.id}/", json=payload)
        assert response.status_code == 200

    async def test_update_doctor_with_inspections(
        self,
        superuser_client: AsyncClient,
        doctor: Doctor,
        gen_doctor_payload,
        doctor_speciality: Speciality,
        doctor_department: Department,
        inspections: list[Inspection],
    ):
        payload = gen_doctor_payload(doctor_speciality.id, doctor_department.id)
        payload["inspections"] = [{"id": inspection.id} for inspection in inspections]
        response = await superuser_client.patch(
            f"/api/doctors/{doctor.id}/", json=payload
        )
        data = response.json()
        assert response.status_code == 200
        assert len(data["inspections"]) == len(inspections)

    async def test_update_doctor_with_unexist_inspections(
        self,
        superuser_client: AsyncClient,
        doctor: Doctor,
        gen_doctor_payload,
        doctor_speciality: Speciality,
        doctor_department: Department,
        inspection: Inspection,
    ):
        payload = gen_doctor_payload(doctor_speciality.id, doctor_department.id)
        payload["inspections"] = [{"id": inspection.id}, {"id": 9999}]
        response = await superuser_client.patch(
            f"/api/doctors/{doctor.id}/", json=payload
        )
        assert response.status_code == 400

    async def test_update_doctor_with_unexist_speciality(
        self,
        superuser_client: AsyncClient,
        doctor: Doctor,
        gen_doctor_payload,
        doctor_department: Department,
    ):
        payload = gen_doctor_payload(9999, doctor_department.id)
        response = await superuser_client.patch(
            f"/api/doctors/{doctor.id}/", json=payload
        )
        assert response.status_code == 400

    async def test_update_doctor_with_unexist_department(
        self,
        superuser_client: AsyncClient,
        doctor: Doctor,
        gen_doctor_payload,
        doctor_speciality: Speciality,
    ):
        payload = gen_doctor_payload(doctor_speciality.id, 9999)
        response = await superuser_client.patch(
            f"/api/doctors/{doctor.id}/", json=payload
        )
        assert response.status_code == 400

    @pytest.mark.parametrize("payload", list(gen_invalid_payload()))
    async def test_update_doctor_invalid_payload(
        self, superuser_client: AsyncClient, doctor: Doctor, payload
    ):
        response = await superuser_client.patch(
            f"/api/doctors/{doctor.id}/", json=payload
        )
        assert response.status_code == 422 or response.status_code == 400

    @pytest.mark.parametrize("payload", patch_payload)
    async def test_patch_doctor(
        self, superuser_client: AsyncClient, doctor: Doctor, payload
    ):
        response = await superuser_client.patch(
            f"/api/doctors/{doctor.id}/", json=payload
        )
        assert response.status_code == 200

    async def test_patch_doctor_photo(
        self, superuser_client: AsyncClient, doctor: Doctor
    ):
        payload = {"photo": other_image_link}
        response = await superuser_client.patch(
            f"/api/doctors/{doctor.id}/", json=payload
        )
        data = response.json()
        assert response.status_code == 200
        assert data["photo"] == payload["photo"]

    async def test_patch_doctor_invalid_photo(
        self, superuser_client: AsyncClient, doctor: Doctor
    ):
        payload = {"photo": "http://invalid.com"}
        response = await superuser_client.patch(
            f"/api/doctors/{doctor.id}/", json=payload
        )
        assert response.status_code == 400

    async def test_delete_doctor_unauth_(self, client: AsyncClient, doctor: Doctor):
        response = await client.delete(f"/api/doctors/{doctor.id}/")
        assert response.status_code == 401

    async def test_delete_doctor_user_role(
        self, user_client: AsyncClient, doctor: Doctor
    ):
        response = await user_client.delete(f"/api/doctors/{doctor.id}/")
        assert response.status_code == 403

    async def test_delete_doctor_admin_role(
        self, admin_client: AsyncClient, doctor: Doctor
    ):
        response = await admin_client.delete(f"/api/doctors/{doctor.id}/")
        assert response.status_code == 204

    async def test_delete_doctor_superuser_role(
        self, superuser_client: AsyncClient, doctor: Doctor
    ):
        response = await superuser_client.delete(f"/api/doctors/{doctor.id}/")
        assert response.status_code == 204
