import pytest

from src.repositories.inspections import InspectionRepository


@pytest.fixture
async def inspection(session):
    repository = InspectionRepository(session)
    payload = {
        "title": "title",
        "description": "description",
        "preparation": "preparation",
    }
    yield await repository.create(payload)
