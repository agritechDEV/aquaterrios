"""empty message

Revision ID: dedd1c83a6db
Revises: 3c5bf03fe1e2
Create Date: 2023-02-06 19:46:04.321682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dedd1c83a6db'
down_revision = '3c5bf03fe1e2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dev_id', sa.String(length=25), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subscriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mail', sa.String(length=50), nullable=True),
    sa.Column('date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.String(length=25), nullable=False),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('read', sa.Boolean(), nullable=True),
    sa.Column('date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user'], ['users.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pumps',
    sa.Column('pump_id', sa.String(length=25), nullable=False),
    sa.Column('system_id', sa.Integer(), nullable=False),
    sa.Column('capacity', sa.Float(), nullable=True),
    sa.Column('available', sa.Float(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['system_id'], ['systems.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('pump_id'),
    sa.UniqueConstraint('pump_id')
    )
    op.create_table('shifts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('system_id', sa.Integer(), nullable=False),
    sa.Column('mode', sa.String(length=25), nullable=False),
    sa.Column('sensors_settings', sa.String(length=25), nullable=False),
    sa.Column('turn_on', sa.Float(), nullable=True),
    sa.Column('turn_off', sa.Float(), nullable=True),
    sa.Column('mon', sa.Boolean(), nullable=True),
    sa.Column('tue', sa.Boolean(), nullable=True),
    sa.Column('wed', sa.Boolean(), nullable=True),
    sa.Column('thu', sa.Boolean(), nullable=True),
    sa.Column('fri', sa.Boolean(), nullable=True),
    sa.Column('sat', sa.Boolean(), nullable=True),
    sa.Column('sun', sa.Boolean(), nullable=True),
    sa.Column('start', sa.Time(), nullable=True),
    sa.Column('stop', sa.Time(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['system_id'], ['systems.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('flow_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pump_id', sa.String(length=25), nullable=False),
    sa.Column('flow', sa.Float(), nullable=True),
    sa.Column('date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['pump_id'], ['pumps.pump_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sensors',
    sa.Column('sensor_id', sa.String(length=25), nullable=False),
    sa.Column('system_id', sa.Integer(), nullable=False),
    sa.Column('shift_id', sa.Integer(), nullable=True),
    sa.Column('readings', sa.Float(), nullable=True),
    sa.Column('set_lvl_1', sa.Boolean(), nullable=True),
    sa.Column('set_lvl_2', sa.Boolean(), nullable=True),
    sa.Column('set_lvl_3', sa.Boolean(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['shift_id'], ['shifts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['system_id'], ['systems.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('sensor_id'),
    sa.UniqueConstraint('sensor_id')
    )
    op.create_table('valves',
    sa.Column('valve_id', sa.String(length=25), nullable=False),
    sa.Column('system_id', sa.Integer(), nullable=False),
    sa.Column('shift_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('mode', sa.String(length=25), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['shift_id'], ['shifts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['system_id'], ['systems.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('valve_id'),
    sa.UniqueConstraint('valve_id')
    )
    op.create_table('sensor_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sensor_id', sa.String(length=25), nullable=False),
    sa.Column('level_1', sa.Float(), nullable=True),
    sa.Column('level_2', sa.Float(), nullable=True),
    sa.Column('level_3', sa.Float(), nullable=True),
    sa.Column('temperature', sa.Float(), nullable=True),
    sa.Column('moisture', sa.Float(), nullable=True),
    sa.Column('bat_level', sa.Float(), nullable=True),
    sa.Column('date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['sensor_id'], ['sensors.sensor_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('systems', 'delisted')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('systems', sa.Column('delisted', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False))
    op.drop_table('sensor_data')
    op.drop_table('valves')
    op.drop_table('sensors')
    op.drop_table('flow_data')
    op.drop_table('shifts')
    op.drop_table('pumps')
    op.drop_table('notifications')
    op.drop_table('subscriptions')
    op.drop_table('logs')
    # ### end Alembic commands ###
