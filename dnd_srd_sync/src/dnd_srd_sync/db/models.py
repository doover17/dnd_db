"""Database models for SRD sync."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Index, Text, UniqueConstraint
from sqlmodel import Field, SQLModel


class ImportRun(SQLModel, table=True):
    """Track ETL import runs."""

    __tablename__ = "import_runs"

    id: Optional[int] = Field(default=None, primary_key=True)
    started_at: datetime = Field(index=True)
    finished_at: Optional[datetime] = Field(default=None, index=True)
    source_name: str = Field(index=True)
    source_version: str = Field(index=True)
    notes: Optional[str] = Field(default=None, sa_column=Column(Text))


class EntitiesRaw(SQLModel, table=True):
    """Raw JSON payloads from source imports."""

    __tablename__ = "entities_raw"
    __table_args__ = (
        UniqueConstraint("entity_type", "source_key", name="uq_entities_raw_type_key"),
        Index("ix_entities_raw_type_key", "entity_type", "source_key"),
        Index("ix_entities_raw_last_seen", "last_seen_run_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    entity_type: str = Field(index=True)
    source_key: str = Field(index=True)
    json: str = Field(sa_column=Column(Text))
    sha256: str = Field(index=True)
    last_seen_run_id: Optional[int] = Field(
        default=None, foreign_key="import_runs.id", index=True
    )


class Spell(SQLModel, table=True):
    """Typed spell records."""

    __tablename__ = "spells"

    id: Optional[int] = Field(default=None, primary_key=True)
    index: str = Field(index=True, unique=True)
    name: str = Field(index=True)
    level: int = Field(index=True)
    school: str = Field(index=True)
    casting_time: str = Field(index=True)
    range: str
    duration: str = Field(index=True)
    concentration: bool = Field(default=False, index=True)
    ritual: bool = Field(default=False, index=True)
    description: str = Field(sa_column=Column(Text))
    higher_level: Optional[str] = Field(default=None, sa_column=Column(Text))


class Class(SQLModel, table=True):
    """Typed class records."""

    __tablename__ = "classes"

    id: Optional[int] = Field(default=None, primary_key=True)
    index: str = Field(index=True, unique=True)
    name: str = Field(index=True)
    hit_die: int = Field(index=True)


class Feature(SQLModel, table=True):
    """Typed feature records."""

    __tablename__ = "features"

    id: Optional[int] = Field(default=None, primary_key=True)
    index: str = Field(index=True, unique=True)
    name: str = Field(index=True)
    level: int = Field(index=True)
    class_index: Optional[str] = Field(default=None, index=True)
    description: str = Field(sa_column=Column(Text))


class Item(SQLModel, table=True):
    """Typed item records."""

    __tablename__ = "items"

    id: Optional[int] = Field(default=None, primary_key=True)
    index: str = Field(index=True, unique=True)
    name: str = Field(index=True)
    equipment_category: str = Field(index=True)
    cost: Optional[str] = Field(default=None, index=True)
    weight: Optional[float] = Field(default=None, index=True)
    description: Optional[str] = Field(default=None, sa_column=Column(Text))


class ClassSpell(SQLModel, table=True):
    """Join table between classes and spells."""

    __tablename__ = "class_spells"
    __table_args__ = (
        UniqueConstraint("class_id", "spell_id", name="uq_class_spells"),
        Index("ix_class_spells_class", "class_id"),
        Index("ix_class_spells_spell", "spell_id"),
    )

    class_id: int = Field(foreign_key="classes.id", primary_key=True)
    spell_id: int = Field(foreign_key="spells.id", primary_key=True)


class ClassFeature(SQLModel, table=True):
    """Join table between classes and features."""

    __tablename__ = "class_features"
    __table_args__ = (
        UniqueConstraint("class_id", "feature_id", name="uq_class_features"),
        Index("ix_class_features_class", "class_id"),
        Index("ix_class_features_feature", "feature_id"),
    )

    class_id: int = Field(foreign_key="classes.id", primary_key=True)
    feature_id: int = Field(foreign_key="features.id", primary_key=True)
