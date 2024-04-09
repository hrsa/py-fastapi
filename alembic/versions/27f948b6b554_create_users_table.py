"""create users table

Revision ID: 27f948b6b554
Revises: eb6faeacd2d8
Create Date: 2024-04-09 14:31:57.927250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '27f948b6b554'
down_revision: Union[str, None] = 'eb6faeacd2d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
                    sa.Column("email", sa.String(), nullable=False, unique=True),
                    sa.Column("name", sa.String(), nullable=True),
                    sa.Column('password', sa.String(length=255), nullable=False),
                    sa.Column("created_at", sa.DateTime(),
                              server_default=sa.text('now()'), nullable=False)
                    )


def downgrade() -> None:
    op.drop_table("users")
