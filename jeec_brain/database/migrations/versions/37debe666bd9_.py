"""empty message

Revision ID: 37debe666bd9
Revises: 8817d4097dcc
Create Date: 2022-03-10 19:11:43.518130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "37debe666bd9"
down_revision = "8817d4097dcc"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("companies", "evf_username")
    op.drop_column("companies", "evf_password")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "companies",
        sa.Column("evf_password", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "companies",
        sa.Column("evf_username", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    # ### end Alembic commands ###
