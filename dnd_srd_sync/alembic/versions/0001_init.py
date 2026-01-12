"""init

Revision ID: 0001_init
Revises: 
Create Date: 2025-02-14 00:00:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "srditem",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("index", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_srditem_index"), "srditem", ["index"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_srditem_index"), table_name="srditem")
    op.drop_table("srditem")
