""" ajout colonne user_id dans table valeursFichier 

Revision ID: 700fb698cb2f
Revises: 87ed49c58364
Create Date: 2023-04-09 01:47:34.916912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '700fb698cb2f'
down_revision = '87ed49c58364'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('valeurs_fichier', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('valeurs_fichier', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
