"""Add chat and message models

Revision ID: e3e42023fbe3
Revises: 9c4986ef1622
Create Date: 2026-09-09 15:48:38.325391

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e3e42023fbe3'
down_revision: Union[str, Sequence[str], None] = '9c4986ef1622'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('chat',
    sa.Column('chat_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.Column('buyer_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['buyer_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['car_id'], ['cars.car_id'], ),
    sa.PrimaryKeyConstraint('chat_id'),
    sa.UniqueConstraint('car_id', 'buyer_id')
    )
    op.create_table('message',
    sa.Column('message_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['chat_id'], ['chat.chat_id'], ),
    sa.PrimaryKeyConstraint('message_id')
    )
    op.add_column('cars', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'cars', 'users', ['owner_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'cars', type_='foreignkey')
    op.drop_column('cars', 'owner_id')
    op.drop_table('message')
    op.drop_table('chat')
