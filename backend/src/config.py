from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ALLOWED_HOSTS: str | None = None
    DEBUG: bool = False
    PAGINATION_SIZE: int = 6

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env", frozen=True)

    @property
    def origins(self):
        origins = ["127.0.0.1", "localhost"]
        if self.ALLOWED_HOSTS:
            origins = self.ALLOWED_HOSTS.split(" ,")
        return origins

    @property
    def DATABASE_URL_ASYNCPG(self):
        return (
            "postgresql+asyncpg:"
            f"//{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}"
            f"/{self.POSTGRES_DB}"
        )

    @property
    def DATABASE_URL_AIOSQLITE(self):
        return "sqlite+aiosqlite:///db.sqlite3"


settings = Settings()  # type: ignore
