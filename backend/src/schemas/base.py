from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        str_min_length=1,
        str_max_length=100000,
    )
