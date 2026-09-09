"""create posts table

Revision ID: 4067d76f8278
Revises: 
Create Date: 2026-07-05 14:41:01.159450

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4067d76f8278'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("title", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
