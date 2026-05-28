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
]
