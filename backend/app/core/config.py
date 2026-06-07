from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    backend_host: str = Field(default="0.0.0.0", alias="SMART_RESUME_BACKEND_HOST")
    backend_port: int = Field(default=8000, alias="SMART_RESUME_BACKEND_PORT")
    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/smart_resume_python",
        alias="SMART_RESUME_DATABASE_URL",
    )
    token_secret: str = Field(default="change-this-secret", alias="SMART_RESUME_TOKEN_SECRET")
    token_expire_days: int = Field(default=30, alias="SMART_RESUME_TOKEN_EXPIRE_DAYS")
    cors_origins: str = Field(default="http://localhost:3789", alias="SMART_RESUME_CORS_ORIGINS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
