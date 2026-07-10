"""from id to car_id

Revision ID: 0f97d984a356
Revises: 6119cec6793d
Create Date: 2026-06-17 14:35:22.341887

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0f97d984a356"
down_revision: Union[str, Sequence[str], None] = "6119cec6793d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("cars", sa.Column("car_id", sa.Integer(), nullable=False))
    op.drop_column("cars", "id")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "cars", sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False)
    )
    op.drop_column("cars", "car_id")
