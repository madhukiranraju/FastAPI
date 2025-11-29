"""create createdby and ownerid

Revision ID: 3564b0777a47
Revises: 6628e70cb30b
Create Date: 2025-11-28 22:39:19.734351

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3564b0777a47'
down_revision: Union[str, Sequence[str], None] = '6628e70cb30b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('created_by', sa.String, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'created_by')
    pass
