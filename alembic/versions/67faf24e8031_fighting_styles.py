"""Fighting styles

Revision ID: 67faf24e8031
Revises: 130ff2281e5e
Create Date: 2025-03-03 00:43:54.377732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67faf24e8031'
down_revision: Union[str, None] = '130ff2281e5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Use batch mode for altering tables in SQLite
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column("fight_style", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("last_fight_style_selection", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("last_fight_time", sa.String(), nullable=True))

    # Create foreign key for 'community_market' table
    op.create_foreign_key("fk_community_market_user", "community_market", "users", ["user_id"], ["id"])


def downgrade() -> None:
    # Use batch mode to drop columns in SQLite
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("last_fight_time")
        batch_op.drop_column("last_fight_style_selection")
        batch_op.drop_column("fight_style")

    # Drop foreign key constraint
    op.drop_constraint("fk_community_market_user", "community_market", type_="foreignkey")

    # ### end Alembic commands ###
