"""empty message

Revision ID: eb8a51633709
Revises: 7793d5f6f23f
Create Date: 2022-03-12 20:07:22.988422

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "eb8a51633709"
down_revision = "7793d5f6f23f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(
        "uix_student_activities", "student_activities", ["student_id", "activity_id"]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("uix_student_activities", "student_activities", type_="unique")
    # ### end Alembic commands ###
