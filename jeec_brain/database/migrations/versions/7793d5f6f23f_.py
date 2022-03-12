"""empty message

Revision ID: 7793d5f6f23f
Revises: 37debe666bd9
Create Date: 2022-03-12 18:16:24.392896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7793d5f6f23f"
down_revision = "37debe666bd9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("company_activities", "zoom_link")
    op.drop_column("company_users", "evf_password")
    op.drop_column("company_users", "evf_username")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "company_users",
        sa.Column("evf_username", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "company_users",
        sa.Column("evf_password", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "company_activities",
        sa.Column("zoom_link", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    # ### end Alembic commands ###
