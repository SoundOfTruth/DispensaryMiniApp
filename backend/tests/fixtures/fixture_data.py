import pytest

from tests.utils import FakerSingleton


@pytest.fixture(scope="session")
def faker():
    return FakerSingleton()
