"""add user_id to posts table

Revision ID: bb1d661d8454
Revises: 27f948b6b554
Create Date: 2024-04-09 14:49:35.616663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb1d661d8454'
down_revision: Union[str, None] = '27f948b6b554'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('author_id', sa.Integer(), nullable=False))
    op.create_foreign_key("posts_user_fk", "posts",
                          "users", ["author_id"],
                          ["id"], ondelete="CASCADE", onupdate="CASCADE")


def downgrade() -> None:
    op.drop_constraint("posts_user_fk", "posts")
    op.drop_column("posts", "author_id")

