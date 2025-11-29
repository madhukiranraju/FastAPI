"""create owner_id column in posts table

Revision ID: 3a6ad2c8d0a7
Revises: fda0118f5406
Create Date: 2025-11-28 22:50:59.174659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a6ad2c8d0a7'
down_revision: Union[str, Sequence[str], None] = 'fda0118f5406'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'owner_id')
    pass
