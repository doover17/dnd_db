"""Configuration helpers for dnd_srd_sync."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

ENV_PATH = Path(".env")


def load_environment() -> None:
    """Load environment variables from a .env file if present."""
    if ENV_PATH.exists():
        load_dotenv(ENV_PATH)


class Settings(BaseModel):
    """Settings loaded from environment variables."""

    db_path: str
    api_base_url: str
    request_timeout_secs: int
    retry_max_attempts: int
    rate_limit_rps: int

    @classmethod
    def from_env(cls) -> "Settings":
        load_environment()
        return cls(
            db_path=os.getenv("DB_PATH", "./data/srd.sqlite"),
            api_base_url=os.getenv("API_BASE_URL", "https://www.dnd5eapi.co"),
            request_timeout_secs=os.getenv("REQUEST_TIMEOUT_SECS", "30"),
            retry_max_attempts=os.getenv("RETRY_MAX_ATTEMPTS", "5"),
            rate_limit_rps=os.getenv("RATE_LIMIT_RPS", "5"),
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings instance loaded from the environment."""
    return Settings.from_env()
