"""add created_at column to post table

Revision ID: 6830d0e1a7c8
Revises: 5c0ad3958a07
Create Date: 2025-01-12 01:51:22.854258

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6830d0e1a7c8'
down_revision: Union[str, None] = '5c0ad3958a07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")))
    pass


def downgrade() -> None:
    op.drop_column("posts", "created_at")
    pass
