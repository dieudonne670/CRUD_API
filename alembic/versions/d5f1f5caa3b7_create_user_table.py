"""create user table

Revision ID: d5f1f5caa3b7
Revises: e2833284f646
Create Date: 2026-07-06 17:09:47.933168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5f1f5caa3b7'
down_revision: Union[str, Sequence[str], None] = 'e2833284f646'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("email", sa.String, unique=True, nullable=False),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    pass
