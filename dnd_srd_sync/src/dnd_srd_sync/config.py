"""Configuration helpers for dnd_srd_sync."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ENV_PATH = Path(".env")


def load_environment() -> None:
    """Load environment variables from a .env file if present."""
    if ENV_PATH.exists():
        load_dotenv(ENV_PATH)


@dataclass(slots=True)
class Settings:
    """Settings loaded from environment variables."""

    db_path: Path
    api_base_url: str

    @property
    def db_url(self) -> str:
        return f"sqlite:///{self.db_path}"

    @classmethod
    def from_env(cls) -> "Settings":
        load_environment()
        db_path = Path(os.getenv("DB_PATH", "dnd_srd.db"))
        api_base_url = os.getenv("API_BASE_URL", "https://www.dnd5eapi.co")
        return cls(db_path=db_path, api_base_url=api_base_url)
