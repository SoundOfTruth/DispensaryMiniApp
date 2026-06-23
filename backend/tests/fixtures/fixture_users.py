import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import Role, User
from src.schemas.users import CreateUserSchema
from src.utils.auth import hash_password


@pytest.fixture(scope="session")
def password():
    return "testpassword"


@pytest.fixture(scope="session")
def gen_user_payload(password, faker):
    def wrapper(role: str):
        user_payload = {
            "email": faker.unique.email(),
            "firstname": faker.first_name(),
            "lastname": faker.last_name(),
            "middlename": faker.last_name(),
            "password": password,
            "role": role,
        }
        return user_payload

    return wrapper


@pytest.fixture(scope="session")
def create_user_instance(gen_user_payload):
    def wrapper(role: Role):
        payload = gen_user_payload(role.value)
        payload["password"] = hash_password(payload["password"])
        schema = CreateUserSchema.model_validate(payload)
        return User(**schema.model_dump())

    return wrapper


@pytest_asyncio.fixture
async def create_user(session: AsyncSession, create_user_instance):
    async def wrapper(role: Role):
        instance = create_user_instance(role)
        session.add(instance)
        await session.commit()
        return instance

    return wrapper


@pytest_asyncio.fixture
async def user(create_user):
    user = await create_user(Role.USER)
    return user


@pytest_asyncio.fixture
async def another_user(create_user):
    user = await create_user(Role.USER)
    return user


@pytest_asyncio.fixture
async def admin(create_user):
    user = await create_user(Role.ADMIN)
    return user


@pytest_asyncio.fixture
async def superuser(create_user):
    user = await create_user(Role.SUPERUSER)
    return user


@pytest_asyncio.fixture
async def users(session: AsyncSession, create_user_instance):
    instances = [create_user_instance(Role.USER) for _ in range(10)]
    session.add_all(instances)
    await session.commit()
    return instances


@pytest_asyncio.fixture
async def many_users(session: AsyncSession, create_user_instance):
    instances = [create_user_instance(Role.USER) for _ in range(50)]
    session.add_all(instances)
    await session.commit()
    return instances
