import io
from uuid import uuid4

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
    return f"http://localhost:8000/media/{uuid4}/"
