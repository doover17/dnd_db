"""Database migration helpers."""

from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config


def run_migrations(config_path: str | Path | None = None) -> None:
    """Run alembic migrations using the provided config path."""
    resolved_path = Path(config_path) if config_path else Path(__file__).resolve().parents[3] / "alembic.ini"
    alembic_cfg = Config(str(resolved_path))
    command.upgrade(alembic_cfg, "head")
