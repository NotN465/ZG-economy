"""Made columns for users fighting style and his last fight time

Revision ID: 14bc6236755d
Revises: 840e2e508eb9
Create Date: 2025-03-02 19:38:10.258474

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14bc6236755d'
down_revision: Union[str, None] = 'c75b86917e1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
