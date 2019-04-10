"""Create CauseUser Table

Revision ID: f77539b0c496
Revises: 6f57bc1476cb
Create Date: 2019-03-14 14:35:49.554252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f77539b0c496'
down_revision = None

branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'use
        sa.Column('id_user',sa.Integer, primary_key=True),
        sa.Column('Prénon/nom',sa.String(15)),
        sa.Column('slack_name',sa.String(15)),
        sa.Column('slack_id',sa.String(10)),
        sa.Column('last_activity',sa.DateTime),
        sa.Column('job',sa.String(255)),
        sa.Column('last_match',sa.String(255)),
    )
    op.create_table(
        'causes',
        sa.Column('id',sa.Integer, primary_key=True),
        sa.Column('name',sa.String(40)),

    )
    op.create_table(
       'user_cause',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id_user', onupdate="CASCADE", ondelete="CASCADE"), nullable=None), 
        sa.Column('cause_id',sa.Integer, sa.ForeignKey('causes.id_cause',onupdate="CASCADE", ondelete="CASCADE"),nullable=None),
        sa.PrimaryKeyConstraint('cause_id', 'user_id', name='user_cause_pk')
    )

    op.create_table(
       'planning',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('day',sa.DateTime),
        sa.Column('value',sa.String(20))
    )

def downgrade():
    op.drop_table('users') 
    op.drop_table('causes')
    op.drop_table('user_cause')
