"""delete autoincrement flag from role id

Revision ID: 6671937cea24
Revises: 883acac4b1fa
Create Date: 2025-05-29 14:38:11.495260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6671937cea24'
down_revision: Union[str, None] = '883acac4b1fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        table_name='roles',
        column_name='id',
        type_=sa.Integer,
        autoincrement=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        table_name='roles',
        column_name='id',
        type_=sa.Integer,
        autoincrement=True
    )
    # ### end Alembic commands ###
