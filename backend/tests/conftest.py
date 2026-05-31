from alembic import command
from alembic.config import Config

from src.config import settings

alembic_config = Config("alembic.ini")
alembic_config.set_main_option("sqlalchemy.url", settings.DATABASE.URL_TEST_ASYNCPG)


def pytest_configure():
    command.upgrade(alembic_config, "head")


def pytest_unconfigure():
    command.downgrade(alembic_config, "base")


pytest_plugins = [
    "tests.fixtures.fixture_db",
    "tests.fixtures.fixture_clients",
    "tests.fixtures.fixture_users",
    "tests.fixtures.fixture_doctors",
    "tests.fixtures.fixture_inspections",
    "tests.fixtures.fixture_equipments",
    "tests.fixtures.fixture_specialties",
    "tests.fixtures.fixture_departments",
    "tests.fixtures.fixture_equipment_types",
    "tests.fixtures.fixture_image",
]
