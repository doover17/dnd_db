"""Database migration helpers."""

from alembic import command
from alembic.config import Config


def run_migrations(config_path: str = "alembic.ini") -> None:
    """Run alembic migrations using the provided config path."""
    alembic_cfg = Config(config_path)
    command.upgrade(alembic_cfg, "head")
