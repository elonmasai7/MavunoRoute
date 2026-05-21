from functools import lru_cache
from typing import Literal

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: Literal["development", "staging", "production", "test"] = "development"
    app_name: str = "MavunoRoute AI"
    app_secret_key: str = Field("change-this-app-secret-in-production-32+", min_length=32)
    api_prefix: str = "/api/v1"
    debug: bool = True

    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/mavunoroute"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret_key: str = Field("change-this-jwt-secret-in-production-32+", min_length=32)
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 14
    jwt_algorithm: str = "HS256"

    cors_allowed_origins: list[AnyHttpUrl] | list[str] = []

    mpesa_consumer_key: str | None = None
    mpesa_consumer_secret: str | None = None
    mpesa_shortcode: str | None = None
    mpesa_passkey: str | None = None
    mpesa_callback_url: str | None = None
    mpesa_environment: str | None = None
    mpesa_callback_secret: str | None = None

    routing_provider: str = "osrm"
    osrm_base_url: str | None = "https://router.project-osrm.org"

    weather_provider: str = "openweather"
    openweather_api_key: str | None = None

    sms_provider: str | None = None
    email_host: str | None = None
    email_port: int = 587
    email_username: str | None = None
    email_password: str | None = None
    email_from: str | None = None

    storage_provider: str = "local"
    local_storage_path: str = "./storage"

    rate_limit_auth_per_minute: int = 10
    rate_limit_public_per_minute: int = 60


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
