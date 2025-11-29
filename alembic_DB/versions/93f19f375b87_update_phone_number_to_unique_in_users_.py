"""update phone number to unique in users table

Revision ID: 93f19f375b87
Revises: a5027e101de8
Create Date: 2025-11-28 23:03:26.559861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93f19f375b87'
down_revision: Union[str, Sequence[str], None] = 'a5027e101de8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint('uq_users_phone_number', 'users', ['phone_number'])
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('uq_users_phone_number', 'users', type_='unique')
    pass
