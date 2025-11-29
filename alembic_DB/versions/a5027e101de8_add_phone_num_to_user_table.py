"""add phone num to user table

Revision ID: a5027e101de8
Revises: 06b3f7557553
Create Date: 2025-11-28 23:00:37.902618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5027e101de8'
down_revision: Union[str, Sequence[str], None] = '06b3f7557553'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String, nullable=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')
    pass
