"""added timer shift relations

Revision ID: 4395275559b3
Revises: aa08ebdad689
Create Date: 2023-09-20 21:38:07.133020

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4395275559b3'
down_revision = 'aa08ebdad689'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('timers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('shift_id', sa.Integer(), nullable=False),
    sa.Column('Mon', sa.Boolean(), nullable=True),
    sa.Column('Tue', sa.Boolean(), nullable=True),
    sa.Column('Wed', sa.Boolean(), nullable=True),
    sa.Column('Thu', sa.Boolean(), nullable=True),
    sa.Column('Fri', sa.Boolean(), nullable=True),
    sa.Column('Sat', sa.Boolean(), nullable=True),
    sa.Column('Sun', sa.Boolean(), nullable=True),
    sa.Column('starts', sa.Time(), nullable=True),
    sa.Column('stops', sa.Time(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['shift_id'], ['shifts.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('timer_controlers')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('timer_controlers',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('shift_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('starts', postgresql.TIME(), autoincrement=False, nullable=True),
    sa.Column('stops', postgresql.TIME(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('Mon', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('Tue', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('Wed', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('Thu', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('Fri', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('Sat', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('Sun', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['shift_id'], ['shifts.id'], name='timer_controlers_shift_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='timer_controlers_pkey')
    )
    op.drop_table('timers')
    # ### end Alembic commands ###
