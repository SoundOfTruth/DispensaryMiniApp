import io

import pytest
from PIL import Image

from tests.utils import image_link


@pytest.fixture
def image() -> bytes:
    img = Image.new("RGB", (100, 100), "black")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture
def image_url():
    return image_link
