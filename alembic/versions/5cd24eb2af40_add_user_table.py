"""add user table

Revision ID: 5cd24eb2af40
Revises: 6830d0e1a7c8
Create Date: 2025-01-12 01:55:05.276119

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5cd24eb2af40'
down_revision: Union[str, None] = '6830d0e1a7c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", 
                    sa.Column("id", sa.Integer(), nullable=False), 
                    sa.Column("email", sa.String(), nullable=False), 
                    sa.Column("password", sa.String(), nullable=False), 
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), 
                              server_default=sa.text("now()"), nullable=False), 
                    sa.PrimaryKeyConstraint("id"), 
                    sa.UniqueConstraint("email"))
    pass


def downgrade() -> None:
    sa.drop_table("users")
    pass
