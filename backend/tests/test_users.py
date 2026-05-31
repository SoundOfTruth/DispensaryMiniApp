import pytest
from httpx import AsyncClient

from src.models.users import Role, User
from src.schemas.users import UserSchema
from tests.utils import validate_pagination, validate_response_schema

pytestmark = pytest.mark.asyncio


class TestUserApi:
    new_password = "new_test_password"
    incorrect_payload = [
        "",
        {},
        [],
        1,
        1.1,
        {
            "email": "bad_email",
            "firstname": "test",
            "lastname": "test",
            "middlename": "test",
            "password": "testpassword",
            "role": "user",
        },
        {
            "email": "test@example.com",
            "firstname": "",
            "lastname": "test",
            "middlename": "test",
            "password": "bad",
            "role": "user",
        },
        {
            "email": "test@example.com",
            "firstname": "test",
            "lastname": "",
            "middlename": "test",
            "password": "testpassword",
            "role": "user",
        },
        {
            "email": "test@example.com",
            "firstname": "test",
            "lastname": "test",
            "middlename": "",
            "password": "testpassword",
            "role": "user",
        },
        {
            "email": "test@example.com",
            "firstname": "test",
            "lastname": "test",
            "middlename": "test",
            "password": "testpassword",
            "role": "",
        },
        {
            "email": "test@example.com",
            "firstname": "test",
            "lastname": "test",
            "middlename": "test",
            "password": "testpassword",
            "role": "",
        },
    ]
    patch_payload = [
        {"email": "test123@example.com"},
        {"firstname": "test"},
        {"lastname": "test"},
        {"middlename": "test"},
        {"password": "testpassword"},
        {"role": "user"},
        {"firstname": "test", "lastname": "test", "middlename": "test"},
        {
            "email": "test1234@example.com",
            "firstname": "test",
            "lastname": "test",
            "middlename": "test",
        },
        {
            "email": "test1234@example.com",
            "firstname": "test",
            "lastname": "test",
            "middlename": "test",
            "role": "admin",
        },
    ]

    @pytest.mark.parametrize(
        "params",
        [
            {"limit": 2, "offset": 0},
            {"limit": 10, "offset": 10},
            {"limit": 20, "offset": 20},
            {"limit": 50, "offset": 0},
        ],
    )
    async def test_get_users_pagination(
        self,
        superuser_client: AsyncClient,
        many_users: list[User],
        params: dict[str, int],
    ):
        response = await superuser_client.get("/api/users/", params=params)
        data = response.json()
        assert validate_pagination(
            data=data,
            schema=UserSchema,
            fixture_length=len(many_users),
            limit=params["limit"],
            offset=params["offset"],
        )

    async def test_get_users_default_pagination(self, admin_client: AsyncClient, users):
        response = await admin_client.get("/api/users/")
        data = response.json()
        assert validate_pagination(
            data=data,
            schema=UserSchema,
            fixture_length=len(users),
        )

    async def test_get_users_superuser_role(self, superuser_client: AsyncClient):
        response = await superuser_client.get("/api/users/")
        assert response.status_code == 200

    async def test_get_users_admin_role(self, admin_client: AsyncClient):
        response = await admin_client.get("/api/users/")
        assert response.status_code == 200

    async def test_get_users_user_role(self, user_client: AsyncClient):
        response = await user_client.get("/api/users/")
        assert response.status_code == 403

    async def test_get_users_unauth(self, client: AsyncClient):
        response = await client.get("/api/users/")
        assert response.status_code == 401

    async def test_get_user_superuser_role(
        self, superuser_client: AsyncClient, another_user
    ):
        response = await superuser_client.get(f"/api/users/{another_user.id}/")
        assert response.status_code == 200
        assert validate_response_schema(response.json(), UserSchema)

    async def test_get_user_admin_role(self, admin_client: AsyncClient, another_user):
        response = await admin_client.get(f"/api/users/{another_user.id}/")
        assert response.status_code == 200
        assert validate_response_schema(response.json(), UserSchema)

    async def test_get_user_user_role(self, user_client: AsyncClient, another_user):
        response = await user_client.get(f"/api/users/{another_user.id}/")
        assert response.status_code == 403

    async def test_get_user_unauth(self, client: AsyncClient, another_user):
        response = await client.get(f"/api/users/{another_user.id}/")
        assert response.status_code == 401

    async def test_get_user_not_found(self, admin_client: AsyncClient):
        response = await admin_client.get("/api/users/9999/")
        assert response.status_code == 404

    async def test_get_me_superuser_role(
        self, superuser_client: AsyncClient, superuser: User
    ):
        response = await superuser_client.get("/api/users/me/")
        data = response.json()
        assert response.status_code == 200
        assert data["id"] == superuser.id
        assert validate_response_schema(data, UserSchema)

    async def test_get_me_admin_role(self, admin_client: AsyncClient, admin: User):
        response = await admin_client.get("/api/users/me/")
        data = response.json()
        assert response.status_code == 200
        assert data["id"] == admin.id

    async def test_get_me_user_role(self, user_client: AsyncClient, user: User):
        response = await user_client.get("/api/users/me/")
        data = response.json()
        assert response.status_code == 200
        assert data["id"] == user.id

    async def test_get_me_unauth(self, client: AsyncClient):
        response = await client.get("/api/users/me/")
        assert response.status_code == 401

    async def test_create_user_uanauth(self, client: AsyncClient, gen_user_payload):
        payload = gen_user_payload(Role.USER.value)
        response = await client.post("/api/users/", data=payload)
        assert response.status_code == 401

    async def test_create_user_empyty_payload(self, superuser_client: AsyncClient):
        response = await superuser_client.post("/api/users/", json={})
        assert response.status_code == 422

    async def test_create_user_superuser_role(
        self, superuser_client: AsyncClient, gen_user_payload
    ):
        payload = gen_user_payload(Role.USER.value)
        response = await superuser_client.post("/api/users/", json=payload)
        assert response.status_code == 201

    async def test_create_admin_superuser_role(
        self, superuser_client: AsyncClient, gen_user_payload
    ):
        payload = gen_user_payload(Role.ADMIN.value)
        response = await superuser_client.post("/api/users/", json=payload)
        assert response.status_code == 201

    async def test_create_superuser_superuser_role(
        self, superuser_client: AsyncClient, gen_user_payload
    ):
        payload = gen_user_payload(Role.SUPERUSER.value)
        response = await superuser_client.post("/api/users/", json=payload)
        assert response.status_code == 201

    async def test_create_user_admin_role(
        self, admin_client: AsyncClient, gen_user_payload
    ):
        payload = gen_user_payload(Role.USER.value)
        response = await admin_client.post("/api/users/", json=payload)
        assert response.status_code == 201

    async def test_create_admin_admin_role(
        self, admin_client: AsyncClient, gen_user_payload
    ):
        payload = gen_user_payload(Role.ADMIN.value)
        response = await admin_client.post("/api/users/", json=payload)
        assert response.status_code == 403

    async def test_create_superuser_admin_role(
        self, admin_client: AsyncClient, gen_user_payload
    ):
        payload = gen_user_payload(Role.SUPERUSER.value)
        response = await admin_client.post("/api/users/", json=payload)
        assert response.status_code == 403

    async def test_create_user_user_role(
        self, user_client: AsyncClient, gen_user_payload
    ):
        payload = gen_user_payload(Role.USER.value)
        response = await user_client.post("/api/users/", json=payload)
        assert response.status_code == 403

    async def test_create_admin_user_role(
        self, user_client: AsyncClient, gen_user_payload
    ):
        payload = gen_user_payload(Role.ADMIN.value)
        response = await user_client.post("/api/users/", json=payload)
        assert response.status_code == 403

    async def test_create_superuser_user_role(
        self, user_client: AsyncClient, gen_user_payload
    ):
        payload = gen_user_payload(Role.SUPERUSER.value)
        response = await user_client.post("/api/users/", json=payload)
        assert response.status_code == 403

    async def test_create_superuser_bad_password(
        self, superuser_client: AsyncClient, gen_user_payload
    ):
        payload = gen_user_payload(Role.SUPERUSER.value)
        payload["password"] = "123"
        response = await superuser_client.post("/api/users/", json=payload)
        assert response.status_code == 422

    async def test_create_user_busy_email(
        self, superuser_client: AsyncClient, superuser: User, gen_user_payload
    ):
        payload = gen_user_payload(Role.USER.value)
        payload["email"] = superuser.email
        response = await superuser_client.post("/api/users/", json=payload)
        assert response.status_code == 400

    @pytest.mark.parametrize("payload", incorrect_payload)
    async def test_create_inspection_incorrect_payload(
        self, superuser_client: AsyncClient, payload
    ):
        response = await superuser_client.post("/api/users/", json=payload)
        assert response.status_code == 422

    async def test_update_busy_email(
        self, superuser_client: AsyncClient, superuser: User, another_user: User
    ):
        payload = {"email": superuser.email}
        response = await superuser_client.patch(
            f"/api/users/{another_user.id}/", json=payload
        )
        assert response.status_code == 400

    async def test_update_empty_payload(
        self, superuser_client: AsyncClient, superuser: User
    ):
        response = await superuser_client.patch(f"/api/users/{superuser.id}/", json={})
        assert response.status_code == 400

    async def test_update_superuser_role(
        self, superuser_client: AsyncClient, another_user, gen_user_payload
    ):
        payload = gen_user_payload(Role.USER.value)
        response = await superuser_client.patch(
            f"/api/users/{another_user.id}/", json=payload
        )
        assert response.status_code == 200
        assert validate_response_schema(response.json(), schema=UserSchema)

    async def test_update_admin_role(
        self, admin_client: AsyncClient, admin, gen_user_payload
    ):
        payload = gen_user_payload(Role.SUPERUSER.value)
        response = await admin_client.patch(f"/api/users/{admin.id}/", json=payload)
        assert response.status_code == 403

    async def test_update_self_password_by_patch(
        self, superuser_client: AsyncClient, superuser: User
    ):
        new_password = "testpassword2"
        response = await superuser_client.patch(
            f"/api/users/{superuser.id}/", json={"password": new_password}
        )
        assert response.status_code == 400

    @pytest.mark.parametrize("payload", patch_payload)
    async def test_patch_update(
        self, superuser_client: AsyncClient, user: User, payload
    ):
        response = await superuser_client.patch(f"/api/users/{user.id}/", json=payload)
        data = response.json()
        assert response.status_code == 200
        assert validate_response_schema(data, schema=UserSchema)
        for key in payload:
            if key != "password":
                assert data[key] == payload[key]

    async def test_change_password_unauth(self, client: AsyncClient, password: str):
        payload = {"current_password": password, "new_password": self.new_password}
        response = await client.post("/api/users/change-password/", json=payload)
        assert response.status_code == 401

    async def test_change_password_fake(self, user_client: AsyncClient):
        payload = {
            "current_password": "fake_password",
            "new_password": self.new_password,
        }
        response = await user_client.post("/api/users/change-password/", json=payload)
        atfter_payload = {
            "current_password": self.new_password,
            "new_password": "fake_password",
        }
        after_response = await user_client.post(
            "/api/users/change-password/", json=atfter_payload
        )
        assert response.status_code == 400
        assert after_response.status_code == 400

    async def test_change_password(self, user_client: AsyncClient, password: str):
        payload = {"current_password": password, "new_password": self.new_password}
        response = await user_client.post("/api/users/change-password/", json=payload)
        atfter_payload = {
            "current_password": self.new_password,
            "new_password": "fake_password",
        }
        after_response = await user_client.post(
            "/api/users/change-password/", json=atfter_payload
        )
        assert response.status_code == 201
        assert after_response.status_code == 201

    async def test_delete_user_role(self, user_client: AsyncClient, superuser: User):
        response = await user_client.delete(f"/api/users/{superuser.id}/")
        assert response.status_code == 403

    async def test_delete_admin_role(self, admin_client: AsyncClient, superuser: User):
        response = await admin_client.delete(f"/api/users/{superuser.id}/")
        assert response.status_code == 403

    async def test_delete_admin_superuser_role(
        self, superuser_client: AsyncClient, admin: User
    ):
        response = await superuser_client.delete(f"/api/users/{admin.id}/")
        assert response.status_code == 204

    async def test_delete_user_superuser_role(
        self, superuser_client: AsyncClient, user: User
    ):
        response = await superuser_client.delete(f"/api/users/{user.id}/")
        assert response.status_code == 204

    async def test_delete_self_superuser(
        self, superuser_client: AsyncClient, superuser: User
    ):
        response = await superuser_client.delete(f"/api/users/{superuser.id}/")
        assert response.status_code == 400
