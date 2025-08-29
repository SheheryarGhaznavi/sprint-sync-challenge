"""first migrations

Revision ID: e12a127d1c50
Revises: 
Create Date: 2025-08-28 21:06:32.283072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e12a127d1c50'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_admin', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.UniqueConstraint('email'),
    )

    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=120), nullable=False),
        sa.Column('description', sa.String(length=4000), nullable=False, server_default=''),
        sa.Column('status', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('total_minutes', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.Index('ix_tasks_title', 'title'),
        sa.Index('ix_tasks_owner', 'user_id'),
    )


def downgrade() -> None:
    op.drop_table('tasks')
    op.drop_table('users')
