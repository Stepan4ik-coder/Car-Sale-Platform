"""New tables

Revision ID: ba8978c58a27
Revises:
Create Date: 2026-06-14 10:55:17.438144

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ba8978c58a27"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "cars",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("engine_type", sa.String(length=100), nullable=False),
        sa.Column("litres", sa.Integer(), nullable=False),
        sa.Column("horse_power", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("color", sa.String(length=100), nullable=False),
        sa.Column("country", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("user")
    op.drop_table("cars")
