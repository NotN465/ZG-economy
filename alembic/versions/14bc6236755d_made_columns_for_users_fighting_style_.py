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
    op.create_table(
        'Combat',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('health', sa.Integer, nullable=False),
        sa.Column('last_hunt_time', sa.String, nullable=True),
        sa.Column('equipment', sa.JSON, nullable=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    )

def downgrade() -> None:
    op.drop_table('Combat')
