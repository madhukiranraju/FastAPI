"""create users table

Revision ID: fda0118f5406
Revises: 3564b0777a47
Create Date: 2025-11-28 22:46:20.923963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fda0118f5406'
down_revision: Union[str, Sequence[str], None] = '3564b0777a47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('email', sa.String, unique=True, nullable=False),  # unique constraint
        sa.Column('password', sa.String, nullable=False),       
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
