from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SmartCampus API"
    api_prefix: str = "/api/v1"
    database_url: str = "postgresql+asyncpg://smartcampus:smartcampus@localhost:5432/smartcampus"
    jwt_secret_key: str = "development-only-change-me"
    jwt_access_token_expire_minutes: int = 30
    cors_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
