"""relationship ActionProgramme Pourquoi5.

Revision ID: ee9d452c3a78
Revises: fd31d24fa0bf
Create Date: 2023-03-24 23:39:25.316217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee9d452c3a78'
down_revision = 'fd31d24fa0bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('action_programme', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pourquoi5_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'pourquoi5', ['pourquoi5_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('action_programme', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('pourquoi5_id')

    # ### end Alembic commands ###
