"""Database engine utilities."""

from sqlmodel import SQLModel, create_engine

from dnd_srd_sync.config import Settings


def get_engine(settings: Settings):
    """Create a SQLModel engine based on settings."""
    return create_engine(settings.db_url, echo=False)


def init_db(engine) -> None:
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)
