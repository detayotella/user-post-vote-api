"""create post table

Revision ID: 5c0ad3958a07
Revises: 
Create Date: 2025-01-12 01:35:39.254917

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c0ad3958a07'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column("title", sa.String(), nullable=False), 
                    sa.Column("content", sa.String(), nullable=False), 
                    sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False))
    pass

def downgrade() -> None:
    op.drop_table("posts") 
    pass
