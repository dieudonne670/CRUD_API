"""add content column to posts table

Revision ID: e2833284f646
Revises: 4067d76f8278
Create Date: 2026-07-06 16:28:20.291089

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2833284f646'
down_revision: Union[str, Sequence[str], None] = '4067d76f8278'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
