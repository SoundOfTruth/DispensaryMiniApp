from logging.config import dictConfig

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    HOST: str = "localhost"
    PORT: int = 5432
    DB: str
    USER: str
    PASSWORD: str

    @property
    def URL_ASYNCPG(self):
        return (
            "postgresql+asyncpg:"
            f"//{self.USER}:{self.PASSWORD}"
            f"@{self.HOST}:{self.PORT}"
            f"/{self.DB}"
        )

    @property
    def URL_TEST_ASYNCPG(self):
        return (
            "postgresql+asyncpg:"
            f"//{self.USER}:{self.PASSWORD}"
            f"@{self.HOST}:{self.PORT}"
            f"/Test{self.DB}"
        )


class Settings(BaseSettings):
    ALLOWED_HOSTS: list[str] = [
        "localhost",
        "localhost:5173",
        "localhost:5174",
        "127.0.0.1",
        "127.0.0.1:5173",
        "127.0.0.1:5174",
        "192.168.0.11",
        "192.168.0.11:5173",
        "192.168.0.11:5174",
    ]

    SECRET: str
    ALGORITM: str = "HS256"
    ACCESS_EXPIRE_MINUTER: int = 15
    REFRESH_EXPIRE_DAYS: int = 30

    DEBUG: bool = False
    PAGINATION_SIZE: int = 10
    MEDIA_DIR: str = "media"
    MEDIA_MAX_SIZE: int = 1024 * 30
    UV_LINK_MODE: str | None = None

    DATABASE: DatabaseSettings = Field(alias="POSTGRES")

    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="_", frozen=True
    )


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(name)s %(message)s",
            "use_colors": False,
        },
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "error.log",
            "formatter": "default",
            "level": "ERROR",
            "mode": "a",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["default"],
            "level": "INFO",
        },
        "error_handler": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}


def configure_logging():
    dictConfig(LOGGING_CONFIG)


settings = Settings()  # type: ignore
