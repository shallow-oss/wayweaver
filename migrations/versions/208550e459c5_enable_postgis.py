"""enable postgis

Revision ID: 208550e459c5
Revises:
Create Date: 2026-07-24 09:33:58.351770
"""

from typing import Sequence, Union

from alembic import op


revision: str = "208550e459c5"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Enable PostGIS spatial database capabilities."""
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")


def downgrade() -> None:
    """Keep the shared PostGIS extension during application rollback."""
    pass