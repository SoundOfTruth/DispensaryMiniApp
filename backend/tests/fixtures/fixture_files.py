import io
import tempfile
import uuid
from pathlib import Path

import pytest
import pytest_asyncio
from PIL import Image

from src.config import settings
from src.models import Doctor, Equipment
from tests.utils import gen_image_url


@pytest.fixture
def image() -> bytes:
    img = Image.new("RGB", (100, 100), "black")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture
def create_temp_files():
    def wrapper(count: int) -> list[str]:
        files = []
        for _ in range(count):
            filename = f"{uuid.uuid4()}.png"
            file_path = Path(settings.MEDIA_DIR) / filename
            file_path.write_bytes(b"test file")
            file_url = f"/{settings.MEDIA_URL}/{filename}"
            files.append(file_url)
        return files

    return wrapper


@pytest.fixture
def image_url():
    return gen_image_url()


@pytest.fixture
def unlinked_files() -> list[str]:
    files = []
    for _ in range(10):
        with tempfile.NamedTemporaryFile(
            dir=settings.MEDIA_DIR,
            suffix=".jpg",
            delete=False,
        ) as tmp:
            tmp.write(b"test file data")
            files.append(tmp.name)
    return files


@pytest_asyncio.fixture
async def linked_files(
    doctors_real_photo: list[Doctor], equipments_real_image: list[Equipment]
) -> list[str]:
    links: list[str] = [equipment.image for equipment in equipments_real_image]
    for doctor in doctors_real_photo:
        if doctor.photo:
            links.append(doctor.photo)
    return links


@pytest_asyncio.fixture
async def any_files(unlinked_files: list[str], linked_files: list[str]) -> list[str]:
    links = unlinked_files.copy()
    links.extend(linked_files)
    return links
