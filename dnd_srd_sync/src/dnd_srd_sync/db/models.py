"""Database models for SRD sync."""

from __future__ import annotations

from typing import Optional

from sqlmodel import Field, SQLModel


class SrdItem(SQLModel, table=True):
    """Generic SRD item placeholder model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    index: str = Field(index=True)
    name: str
    url: str
