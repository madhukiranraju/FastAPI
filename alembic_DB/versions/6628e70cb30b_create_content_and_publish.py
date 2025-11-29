"""create content and publish

Revision ID: 6628e70cb30b
Revises: 9ad00d343852
Create Date: 2025-11-28 22:32:11.102219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6628e70cb30b'
down_revision: Union[str, Sequence[str], None] = '9ad00d343852'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    op.add_column('posts', sa.Column('published', sa.Boolean, server_default='TRUE', nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    op.drop_column('posts', 'published')
    pass
