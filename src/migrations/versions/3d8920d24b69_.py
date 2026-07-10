"""empty message

Revision ID: 3d8920d24b69
Revises: 58ae5eb78027
Create Date: 2026-06-21 14:52:26.208649

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "3d8920d24b69"
down_revision: Union[str, Sequence[str], None] = "58ae5eb78027"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "favorites",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("car_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["car_id"],
            ["cars.car_id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "car_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("favorites")
