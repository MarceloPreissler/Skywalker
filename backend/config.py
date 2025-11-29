from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    database_url: str = Field(
        "sqlite+aiosqlite:///./energy.db",
        description="SQLAlchemy connection string. Defaults to SQLite for local dev.",
    )
    api_key: str = Field(
        "local-dev-key",
        description="API key required to trigger manual scrapes via the REST API.",
    )
    scrape_providers: List[str] = Field(
        default_factory=lambda: [
            "txu",
            "reliant",
            "gexa",
            "direct_energy",
        ],
        description="List of provider slugs to scrape by default.",
    )
    scrape_interval_minutes: int = Field(
        360,
        description="Interval in minutes for scheduled scrapes.",
    )
    scheduler_enabled: bool = Field(
        True,
        description="Toggle background scheduler for recurring scrapes.",
    )

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[1] / ".env",
        env_file_encoding="utf-8",
        env_prefix="",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings()
