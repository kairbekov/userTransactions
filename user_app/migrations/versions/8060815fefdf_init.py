"""init

Revision ID: 8060815fefdf
Revises: 
Create Date: 2022-12-12 07:22:08.284918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8060815fefdf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Text(), nullable=False),
                    sa.Column('name', sa.Text(), nullable=True),
                    sa.Column('surname', sa.Text(), nullable=True),
                    sa.Column('balance', sa.Float(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('transactions',
                    sa.Column('id', sa.Text(), nullable=False),
                    sa.Column('user_id', sa.Text(), nullable=False),
                    sa.Column('transaction_type', sa.Text(), nullable=True),
                    sa.Column('status', sa.Text(), nullable=True),
                    sa.Column('amount', sa.Float(), nullable=True),
                    sa.Column('created_date', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
                    )


def downgrade():
    op.drop_table('users')
    op.drop_table('transactions')
