from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="WAYWEAVER_",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "WayWeaver"
    app_env: Literal[
        "development",
        "test",
        "staging",
        "production",
    ] = "development"
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()