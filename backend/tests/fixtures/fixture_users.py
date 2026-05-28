import pytest
import pytest_asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import Role, User
from src.schemas.users import CreateUserSchema
from src.utils.auth import hash_password

faker = Faker()


@pytest.fixture(scope="session")
def password():
    return "testpassword"


@pytest.fixture(scope="session")
def create_user_data(password):
    def wrapper(role: Role):
        schema = CreateUserSchema(
            email=faker.unique.email(),
            firstname=faker.first_name(),
            lastname=faker.last_name(),
            middlename=faker.unique.user_name(),
            password=hash_password(password),
            role=role,
        )
        return User(**schema.model_dump())

    return wrapper


@pytest_asyncio.fixture
async def create_user(session: AsyncSession, create_user_data):
    async def wrapper(role: Role):
        instance = create_user_data(role)
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
async def users(session: AsyncSession, create_user_data):
    instances = [create_user_data(Role.USER) for _ in range(10)]
    session.add_all(instances)
    await session.commit()
    return instances
