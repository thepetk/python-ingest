"""create events table

Revision ID: e4bbc153c9dd
Revises: 
Create Date: 2020-07-07 16:31:00.867225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4bbc153c9dd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():  
    op.create_table(
        'event',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('device_number', sa.String(), nullable=False),
        sa.Column('event_code', sa.String(), nullable=False),
        sa.Column('message_date', sa.DateTime()),
        sa.Column('longitude', sa.String()),
        sa.Column('latitude', sa.DateTime(), default=sa.func.now()))

    op.create_index(op.f('ix_events_device_number'), 'event', ['device_number'], unique=False)
    op.create_index(op.f('ix_events_event_code'), 'event', ['event_code'], unique=False)
    op.create_index(op.f('ix_events_message_date'), 'event', ['message_date'], unique=False)

def downgrade():  
    op.drop_table('event')