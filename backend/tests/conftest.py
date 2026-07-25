import tempfile

import pytest
from alembic import command
from alembic.config import Config

alembic_config = Config("alembic.ini")
mp = pytest.MonkeyPatch()
temp_dir = tempfile.TemporaryDirectory()
mp.setenv("MEDIA_DIR", temp_dir.name)


def pytest_configure():
    from src.config import settings

    alembic_config.set_main_option("sqlalchemy.url", settings.DATABASE.URL_TEST_ASYNCPG)
    command.upgrade(alembic_config, "head")


def pytest_unconfigure():
    temp_dir.cleanup()
    mp.undo()
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
    "tests.fixtures.fixture_files",
    "tests.fixtures.fixture_data",
]
