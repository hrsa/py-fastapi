"""create posts table

Revision ID: eb6faeacd2d8
Revises: 
Create Date: 2024-04-09 14:15:03.130507

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'eb6faeacd2d8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts",
                    sa.Column('id', sa.Integer, nullable=False, primary_key=True),
                    sa.Column('title', sa.String, nullable=True),
                    sa.Column('content', sa.String, nullable=True),
                    sa.Column('published', sa.Boolean, default=False, nullable=False),
                    sa.Column('rating', sa.Integer, nullable=True),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text("NOW()"), nullable=False)
                    )


def downgrade() -> None:
    op.drop_table(table_name="posts")
