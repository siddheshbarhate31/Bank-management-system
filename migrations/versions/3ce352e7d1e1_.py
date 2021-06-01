"""empty message

Revision ID: 3ce352e7d1e1
Revises: 
Create Date: 2021-05-24 10:58:54.807105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ce352e7d1e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('AccountType',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_type', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('BranchDetails',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('branch_name', sa.String(length=200), nullable=True),
    sa.Column('branch_address', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('FundTransfer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_account', sa.String(length=10), nullable=False),
    sa.Column('to_account', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('TokenBlocklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('TransactionType',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('transaction_type', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('UserType',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_type', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=120), nullable=True),
    sa.Column('last_name', sa.String(length=120), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('mobile_number', sa.String(length=10), nullable=True),
    sa.Column('email_id', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=120), nullable=True),
    sa.Column('is_deleted', sa.Integer(), nullable=True),
    sa.Column('user_type_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_type_id'], ['UserType.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email_id'),
    sa.UniqueConstraint('email_id'),
    sa.UniqueConstraint('mobile_number'),
    sa.UniqueConstraint('mobile_number')
    )
    op.create_table('BankAccount',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_number', sa.String(length=10), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('account_type_id', sa.Integer(), nullable=True),
    sa.Column('branch_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('balance', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['account_type_id'], ['AccountType.id'], ),
    sa.ForeignKeyConstraint(['branch_id'], ['BranchDetails.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('account_number'),
    sa.UniqueConstraint('account_number')
    )
    op.create_table('AccountTransactionDetails',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('transaction_amount', sa.Integer(), nullable=True),
    sa.Column('transaction_date', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('bank_account_id', sa.Integer(), nullable=True),
    sa.Column('transaction_type_id', sa.Integer(), nullable=True),
    sa.Column('fund_id', sa.Integer(), nullable=True),
    sa.Column('transaction_status', sa.String(length=120), nullable=False),
    sa.ForeignKeyConstraint(['bank_account_id'], ['BankAccount.id'], ),
    sa.ForeignKeyConstraint(['fund_id'], ['FundTransfer.id'], ),
    sa.ForeignKeyConstraint(['transaction_type_id'], ['TransactionType.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('AccountTransactionDetails')
    op.drop_table('BankAccount')
    op.drop_table('User')
    op.drop_table('UserType')
    op.drop_table('TransactionType')
    op.drop_table('TokenBlocklist')
    op.drop_table('FundTransfer')
    op.drop_table('BranchDetails')
    op.drop_table('AccountType')
    # ### end Alembic commands ###
