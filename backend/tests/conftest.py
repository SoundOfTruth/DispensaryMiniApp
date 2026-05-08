from alembic import command
from alembic.config import Config

from src.config import settings

alembic_config = Config("alembic.ini")
alembic_config.set_main_option("sqlalchemy.url", settings.DATABASE.URL_TEST_ASYNCPG)


def pytest_configure():
    command.upgrade(alembic_config, "head")

    from src.database.core import async_session_scoped_gen
    from src.main import app
    from tests.core import test_async_session_scoped_generator

    app.dependency_overrides[async_session_scoped_gen] = (
        test_async_session_scoped_generator
    )


def pytest_unconfigure():
    command.downgrade(alembic_config, "base")


pytest_plugins = [
    "tests.fixtures.fixture_data",
    "tests.fixtures.fixture_doctor",
    "tests.fixtures.fixture_inspections",
]
