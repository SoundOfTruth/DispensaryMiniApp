import io

import pytest
from PIL import Image


@pytest.fixture
def image() -> bytes:
    img = Image.new("RGB", (100, 100), "black")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture
def image_url():
    return "http://test/media/9c6e6a46-8586-437b-ac0b-5014048f3b6c.jpeg/"
