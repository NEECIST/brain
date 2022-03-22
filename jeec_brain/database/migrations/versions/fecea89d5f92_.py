"""empty message

Revision ID: fecea89d5f92
Revises: 5d1695f4c3c7
Create Date: 2022-03-07 22:25:36.591034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fecea89d5f92'
down_revision = '5d1695f4c3c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lootbox_rewards', sa.Column('lootbox_id', sa.Integer(), nullable=True))
    op.drop_constraint('lootbox_rewards_lootboxes_id_fkey', 'lootbox_rewards', type_='foreignkey')
    op.create_foreign_key(None, 'lootbox_rewards', 'lootboxes', ['lootbox_id'], ['id'], ondelete='SET NULL')
    op.drop_column('lootbox_rewards', 'lootboxes_id')
    op.add_column('student_lootbox', sa.Column('lootbox_id', sa.Integer(), nullable=True))
    op.drop_constraint('student_lootbox_lootbox_rewards_id_fkey', 'student_lootbox', type_='foreignkey')
    op.create_foreign_key(None, 'student_lootbox', 'lootboxes', ['lootbox_id'], ['id'], ondelete='SET NULL')
    op.drop_column('student_lootbox', 'lootbox_rewards_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student_lootbox', sa.Column('lootbox_rewards_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'student_lootbox', type_='foreignkey')
    op.create_foreign_key('student_lootbox_lootbox_rewards_id_fkey', 'student_lootbox', 'lootbox_rewards', ['lootbox_rewards_id'], ['id'], ondelete='CASCADE')
    op.drop_column('student_lootbox', 'lootbox_id')
    op.add_column('lootbox_rewards', sa.Column('lootboxes_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'lootbox_rewards', type_='foreignkey')
    op.create_foreign_key('lootbox_rewards_lootboxes_id_fkey', 'lootbox_rewards', 'lootboxes', ['lootboxes_id'], ['id'], ondelete='SET NULL')
    op.drop_column('lootbox_rewards', 'lootbox_id')
    # ### end Alembic commands ###
