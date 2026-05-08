import base64
import os
import re
import uuid

import aiofiles

allowed_types = "|".join(["jpeg", "png", "webp", "avif", "svg", "gif", "apng"])


async def save_base64_image(file_data: str):
    pattern = rf"^data:image/({allowed_types});base64,"
    if not re.match(pattern, file_data):
        raise

    format, image = file_data.split(";base64,")
    directory = "media/"
    os.makedirs(directory, exist_ok=True)
    filename = f"{uuid.uuid4()}.{format.split('/')[-1]}"
    filepath = directory + "/" + filename
    try:
        bytes = base64.b64decode(image)
        async with aiofiles.open(filepath, "wb") as f:
            await f.write(bytes)
    except Exception:
        raise
    return filepath
