
"""add user id to ratings

Revision ID: d3230755625d
Revises:
Create Date: 2026-11-15 09:56:25.905035
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd3230755625d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add nullable user_id column
    op.add_column(
        'ratings',
        sa.Column('user_id', sa.Integer(), nullable=True)
    )

    # Create index
    op.create_index(
        'ix_ratings_user_id',
        'ratings',
        ['user_id'],
        unique=False
    )

    # Create named foreign key
    op.create_foreign_key(
        'fk_ratings_user_id_users',
        'ratings',
        'users',
        ['user_id'],
        ['id']
    )


def downgrade() -> None:
    # Remove foreign key
    op.drop_constraint(
        'fk_ratings_user_id_users',
        'ratings',
        type_='foreignkey'
    )

    # Remove index
    op.drop_index(
        'ix_ratings_user_id',
        table_name='ratings'
    )

    # Remove column
    op.drop_column('ratings', 'user_id')
