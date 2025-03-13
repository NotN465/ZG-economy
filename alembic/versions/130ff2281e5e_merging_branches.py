"""Merging branches

Revision ID: 130ff2281e5e
Revises: 14bc6236755d, 76c9d70b4303
Create Date: 2025-03-03 00:41:12.408700

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '130ff2281e5e'
down_revision: Union[str, None] = ('14bc6236755d', '76c9d70b4303')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
