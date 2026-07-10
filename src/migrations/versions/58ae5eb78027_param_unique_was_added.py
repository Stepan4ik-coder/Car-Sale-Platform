"""param unique was added

Revision ID: 58ae5eb78027
Revises: 9da702ba1d02
Create Date: 2026-06-18 16:07:27.139795

"""

from typing import Sequence, Union

from alembic import op


revision: str = "58ae5eb78027"
down_revision: Union[str, Sequence[str], None] = "9da702ba1d02"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
