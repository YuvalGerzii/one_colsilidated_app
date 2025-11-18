"""merge_multiple_heads

Revision ID: 8cc9b37111b7
Revises: 9bced9088006, b9cfe8912345, bb987863a21e
Create Date: 2025-11-14 14:23:32.381152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cc9b37111b7'
down_revision: Union[str, None] = ('9bced9088006', 'b9cfe8912345', 'bb987863a21e')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
