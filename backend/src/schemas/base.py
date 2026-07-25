import re
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict

from src.config import settings
from src.services.exceptions import InvalidImageUrlError

allowed_types = "|".join(["jpeg", "png", "webp", "avif", "apng"])

pattern = re.compile(
    rf"^/{settings.MEDIA_URL}/[0-9a-f]{{8}}-[0-9a-f]{{4}}-4[0-9a-f]{{3}}-[89ab][0-9a-f]{{3}}-[0-9a-f]{{12}}\.(?:{allowed_types})$"
)


def validate_file(value):
    if not re.match(pattern.pattern, value):
        raise InvalidImageUrlError
    return value


FileField = Annotated[str, AfterValidator(validate_file)]


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        str_min_length=1,
        str_max_length=1_000,
    )
