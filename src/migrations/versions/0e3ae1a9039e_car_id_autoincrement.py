"""car_id autoincrement

Revision ID: 0e3ae1a9039e
Revises: 0f97d984a356
Create Date: 2026-06-17 15:31:47.485057

"""

from typing import Sequence, Union


revision: str = "0e3ae1a9039e"
down_revision: Union[str, Sequence[str], None] = "0f97d984a356"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
