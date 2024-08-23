"""empty message

Revision ID: 7cd868130a07
Revises: 7a94e94fc78b
Create Date: 2024-08-23 11:16:02.764806

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7cd868130a07'
down_revision: Union[str, None] = '7a94e94fc78b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('musics', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('musics', 'artist',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('musics', 'path',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('musics', 'hash',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('musics', 'hash',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('musics', 'path',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('musics', 'artist',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('musics', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
