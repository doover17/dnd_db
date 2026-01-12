"""Database engine utilities."""

from pathlib import Path

from sqlmodel import SQLModel, create_engine

from dnd_srd_sync.config import Settings


def get_engine(settings: Settings):
    """Create a SQLModel engine based on settings."""
    db_path = Path(settings.db_path)
    if db_path.is_absolute():
        db_url = f"sqlite:///{db_path.as_posix()}"
    else:
        db_url = f"sqlite:///./{db_path.as_posix()}"
    return create_engine(db_url, echo=False)


def init_db(engine) -> None:
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)
