"""Added lokacija column to the User table

Revision ID: 76f07c528b7f
Revises: 40dbbe156be3
Create Date: 2025-04-12 19:46:49.380051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76f07c528b7f'
down_revision: Union[str, None] = '40dbbe156be3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'community_market', 'users', ['user_id'], ['id'])
    op.add_column('users', sa.Column('lokacija', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'lokacija')
    op.drop_constraint(None, 'community_market', type_='foreignkey')
    # ### end Alembic commands ###
