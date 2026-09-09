"""update Livestreams models

Revision ID: 62a185a83e61
Revises: cf8276882bd7
Create Date: 2026-07-30 21:43:34.893199

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '62a185a83e61'
down_revision: Union[str, Sequence[str], None] = 'cf8276882bd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""

    # Add new thumbnail_url column
    op.add_column(
        "live_streams",
        sa.Column(
            "thumbnail_url",
            sa.String(),
            nullable=True,
        ),
    )

    # Add status column with default value
    op.add_column(
        "live_streams",
        sa.Column(
            "status",
            sa.String(),
            nullable=False,
            server_default="OFFLINE",
        ),
    )

    # Convert description from VARCHAR to TEXT
    op.alter_column(
        "live_streams",
        "description",
        existing_type=sa.VARCHAR(),
        type_=sa.Text(),
        existing_nullable=True,
    )

    # Make sure existing rows don't contain NULL values
    op.execute(
        """
        UPDATE live_streams
        SET
            is_live = COALESCE(is_live, FALSE),
            current_viewers = COALESCE(current_viewers, 0),
            peak_viewers = COALESCE(peak_viewers, 0)
        """
    )

    # Now safely make them NOT NULL
    op.alter_column(
        "live_streams",
        "is_live",
        existing_type=sa.BOOLEAN(),
        nullable=False,
    )

    op.alter_column(
        "live_streams",
        "current_viewers",
        existing_type=sa.INTEGER(),
        nullable=False,
    )

    op.alter_column(
        "live_streams",
        "peak_viewers",
        existing_type=sa.INTEGER(),
        nullable=False,
    )

    op.alter_column(
        "live_streams",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text("now()"),
    )

    # Remove old thumbnail column
    op.drop_column("live_streams", "thumbnail")

    # Remove the database default for future inserts.
    # SQLAlchemy's model default will handle it.
    op.alter_column(
        "live_streams",
        "status",
        server_default=None,
    )