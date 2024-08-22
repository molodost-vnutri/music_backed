"""empty message

Revision ID: afbeed694326
Revises: f31e7e21ce02
Create Date: 2024-08-22 16:06:53.235735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afbeed694326'
down_revision: Union[str, None] = 'f31e7e21ce02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('genre', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('genre')
    )
    op.create_table('musics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('albom', sa.String(), nullable=True),
    sa.Column('artist', sa.String(), nullable=True),
    sa.Column('path', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('path')
    )
    op.create_table('music_genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('music_id', sa.Integer(), nullable=True),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], ),
    sa.ForeignKeyConstraint(['music_id'], ['musics.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.execute("INSERT INTO genres (genre) VALUES ('Hip-hop');")
    op.execute("INSERT INTO genres (genre) VALUES ('Plug');")
    op.execute("INSERT INTO genres (genre) VALUES ('Rap');")
    op.execute("INSERT INTO genres (genre) VALUES ('Electro');")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('music_genres')
    op.drop_table('musics')
    op.drop_table('genres')
    # ### end Alembic commands ###
