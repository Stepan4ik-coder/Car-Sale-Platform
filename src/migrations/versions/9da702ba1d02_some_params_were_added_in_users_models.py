"""Some params were added in users models

Revision ID: 9da702ba1d02
Revises: 19b177ebd16c
Create Date: 2026-06-17 20:49:39.111874

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9da702ba1d02"
down_revision: Union[str, Sequence[str], None] = "19b177ebd16c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("email", sa.String(length=200), nullable=False))
    op.add_column("users", sa.Column("password", sa.String(length=200), nullable=False))
    op.add_column(
        "users", sa.Column("first_name", sa.String(length=100), nullable=False)
    )
    op.add_column(
        "users", sa.Column("last_name", sa.String(length=100), nullable=False)
    )
    op.add_column(
        "users", sa.Column("phone_number", sa.String(length=100), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "phone_number")
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")
    op.drop_column("users", "password")
    op.drop_column("users", "email")
