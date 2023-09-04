"""add foreign key to posts table

Revision ID: 57f10e1429cc
Revises: 7ca2368986ef
Create Date: 2023-08-31 22:13:46.467182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57f10e1429cc'
down_revision: Union[str, None] = '7ca2368986ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post-user-fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post-user-fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
