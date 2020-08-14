"""empty message

Revision ID: 2fd44306cf67
Revises: 
Create Date: 2020-08-14 22:48:38.093574

"""
from alembic import op
import sqlalchemy as sa
import app

# revision identifiers, used by Alembic.
revision = '2fd44306cf67'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist_tokens',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('token', sa.String(length=500), nullable=False),
    sa.Column('blacklisted_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('group',
    sa.Column('_uuid', app.main.model._common.GUID(), nullable=False),
    sa.Column('uuid_creator', app.main.model._common.GUID(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('_uuid'),
    sa.UniqueConstraint('_uuid')
    )
    op.create_table('invitation',
    sa.Column('_uuid', app.main.model._common.GUID(), nullable=False),
    sa.Column('uuid_sender', app.main.model._common.GUID(), nullable=True),
    sa.Column('uuid_invitee', app.main.model._common.GUID(), nullable=True),
    sa.Column('uuid_resource', app.main.model._common.GUID(), nullable=True),
    sa.Column('resource_type', sa.String(length=16), nullable=True),
    sa.Column('status', sa.String(length=16), nullable=True),
    sa.Column('token', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('_uuid'),
    sa.UniqueConstraint('_uuid'),
    sa.UniqueConstraint('token')
    )
    op.create_table('membership',
    sa.Column('_uuid', app.main.model._common.GUID(), nullable=False),
    sa.Column('uuid_member', app.main.model._common.GUID(), nullable=True),
    sa.Column('uuid_resource', app.main.model._common.GUID(), nullable=True),
    sa.Column('resource_type', sa.String(length=16), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('_uuid'),
    sa.UniqueConstraint('_uuid')
    )
    op.create_table('user',
    sa.Column('_uuid', app.main.model._common.GUID(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('registered_on', sa.DateTime(), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password_hash', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('_uuid'),
    sa.UniqueConstraint('_uuid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('membership')
    op.drop_table('invitation')
    op.drop_table('group')
    op.drop_table('blacklist_tokens')
    # ### end Alembic commands ###
