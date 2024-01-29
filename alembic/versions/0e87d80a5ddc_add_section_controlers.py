"""add section controlers

Revision ID: 0e87d80a5ddc
Revises: 3b88f2a7c5d7
Create Date: 2023-09-06 16:35:59.601064

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0e87d80a5ddc'
down_revision = '3b88f2a7c5d7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sensor_controlers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('section_id', sa.Integer(), nullable=True),
    sa.Column('sensor_id', sa.String(length=25), nullable=True),
    sa.Column('starts_at', sa.Float(), nullable=True),
    sa.Column('stops_at', sa.Float(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('timer_controlers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('shift_id', sa.Integer(), nullable=True),
    sa.Column('day', sa.String(length=25), nullable=True),
    sa.Column('starts', sa.Time(), nullable=True),
    sa.Column('stops', sa.Time(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('sections', sa.Column('valve_id', sa.String(length=25), nullable=True))
    op.create_unique_constraint(None, 'sections', ['valve_id'])
    op.drop_column('sensors', 'section_id')
    op.drop_column('shifts', 'Fri')
    op.drop_column('shifts', 'Wed')
    op.drop_column('shifts', 'stop')
    op.drop_column('shifts', 'Tue')
    op.drop_column('shifts', 'Sat')
    op.drop_column('shifts', 'Thu')
    op.drop_column('shifts', 'Sun')
    op.drop_column('shifts', 'start')
    op.drop_column('shifts', 'turn_on')
    op.drop_column('shifts', 'Mon')
    op.drop_column('shifts', 'turn_off')
    op.drop_column('valves', 'section_id')
    op.drop_column('valves', 'mode')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('valves', sa.Column('mode', sa.VARCHAR(length=25), autoincrement=False, nullable=False))
    op.add_column('valves', sa.Column('section_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('shifts', sa.Column('turn_off', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('shifts', sa.Column('Mon', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('shifts', sa.Column('turn_on', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('shifts', sa.Column('start', postgresql.TIME(), autoincrement=False, nullable=True))
    op.add_column('shifts', sa.Column('Sun', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('shifts', sa.Column('Thu', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('shifts', sa.Column('Sat', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('shifts', sa.Column('Tue', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('shifts', sa.Column('stop', postgresql.TIME(), autoincrement=False, nullable=True))
    op.add_column('shifts', sa.Column('Wed', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('shifts', sa.Column('Fri', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('sensors', sa.Column('section_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'sections', type_='unique')
    op.drop_column('sections', 'valve_id')
    op.drop_table('timer_controlers')
    op.drop_table('sensor_controlers')
    # ### end Alembic commands ###
