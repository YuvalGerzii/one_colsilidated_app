"""Add YFinance and Economics API tables only

Revision ID: bb987863a21e
Revises: 8aced9077005
Create Date: 2025-11-13 15:07:04.060379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb987863a21e'
down_revision: Union[str, None] = '8aced9077005'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
