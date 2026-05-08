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
        "http://localhost",
        "http://localhost:5173",
        "http://127.0.0.1",
        "http://127.0.0.1:5173",
        "http://192.168.0.11",
        "http://192.168.0.11:5173",
    ]

    SECRET: str
    ALGORITM: str = "HS256"
    ACCESS_EXPIRE_MINUTER: int = 15
    REFRESH_EXPIRE_DAYS: int = 30

    DEBUG: bool = False
    PAGINATION_SIZE: int = 10
    MEDIA_DIR: str = "media"
    MEDIA_MAX_SIZE: int = 1024 * 30

    DATABASE: DatabaseSettings = Field(alias="POSTGRES")

    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="_", frozen=True
    )


settings = Settings()  # type: ignore
