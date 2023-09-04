"""adding content columen to the table posts

Revision ID: ba711b1613c3
Revises: 117573c62bc4
Create Date: 2023-08-31 21:50:40.025501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba711b1613c3'
down_revision: Union[str, None] = '117573c62bc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
