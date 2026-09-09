"""add location and website to users

Revision ID: 9f1cb2a7e8d4
Revises: d7fdd498738a
Create Date: 2026-08-29 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f1cb2a7e8d4'
down_revision: Union[str, Sequence[str], None] = 'd7fdd498738a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('location', sa.String(), nullable=True))
    op.add_column('users', sa.Column('website', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'website')
    op.drop_column('users', 'location')
