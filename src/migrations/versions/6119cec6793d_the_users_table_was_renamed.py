"""The Users' table was renamed

Revision ID: 6119cec6793d
Revises: ba8978c58a27
Create Date: 2026-06-14 14:02:37.842146

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "6119cec6793d"
down_revision: Union[str, Sequence[str], None] = "ba8978c58a27"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_table("user")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        "user",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("user_pkey")),
    )
    op.drop_table("users")
