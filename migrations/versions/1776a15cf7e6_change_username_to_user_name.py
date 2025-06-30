"""change username to user_name

Revision ID: 1776a15cf7e6
Revises: 6671937cea24
Create Date: 2025-06-27 17:17:49.552501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1776a15cf7e6'
down_revision: Union[str, None] = '6671937cea24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        'users',
        'username',
        new_column_name='user_name',
        existing_type=sa.String(30),
        existing_nullable=False
    )


def downgrade() -> None:
    op.alter_column(
        'users',
        'user_name',
        new_column_name='username',
        existing_type=sa.String(30),
        existing_nullable=False
    )
