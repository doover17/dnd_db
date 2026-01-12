"""Database engine utilities."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import event, text
from sqlmodel import SQLModel, Session, create_engine

from dnd_srd_sync.config import Settings


def _configure_sqlite_pragmas(engine) -> None:
    if engine.url.get_backend_name() != "sqlite":
        return

    @event.listens_for(engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, _connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def get_engine(settings: Settings):
    """Create a SQLModel engine based on settings."""
    engine = create_engine(settings.db_url, echo=False)
    _configure_sqlite_pragmas(engine)
    return engine


@contextmanager
def get_session(settings: Settings) -> Iterator[Session]:
    """Provide a SQLModel session scope."""
    engine = get_engine(settings)
    with Session(engine) as session:
        yield session


def smoke_test(settings: Settings) -> int:
    """Create a session and execute a quick SELECT 1 statement."""
    with get_session(settings) as session:
        return session.exec(text("SELECT 1")).one()[0]


def init_db(engine) -> None:
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)
