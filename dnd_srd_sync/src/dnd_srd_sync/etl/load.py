"""Load normalized data into the database."""

from __future__ import annotations

from typing import Iterable

from sqlmodel import Session

from dnd_srd_sync.db.models import SrdItem


def load_items(session: Session, items: Iterable[dict]) -> int:
    """Persist items to the database and return count."""
    count = 0
    for item in items:
        session.add(SrdItem(**item))
        count += 1
    session.commit()
    return count
