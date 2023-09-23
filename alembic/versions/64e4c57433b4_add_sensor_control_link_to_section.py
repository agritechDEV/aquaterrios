"""add sensor control link to section

Revision ID: 64e4c57433b4
Revises: 0e87d80a5ddc
Create Date: 2023-09-16 12:44:15.774558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64e4c57433b4'
down_revision = '0e87d80a5ddc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sensor_controlers', 'section_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key(None, 'sensor_controlers', 'sections', ['section_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'sensor_controlers', type_='foreignkey')
    op.alter_column('sensor_controlers', 'section_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###