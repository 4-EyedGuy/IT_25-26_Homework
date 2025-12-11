"""initial

Revision ID: 53777a939f6b
Revises: 
Create Date: 2025-12-11 16:53:16.834012

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import Integer, String, Boolean, DateTime, Float
from datetime import datetime
import hashlib
import secrets

revision = 'seed_001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False)
    )

    op.create_table(
        'tokens',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('value', sa.String, nullable=False, unique=True),
        sa.Column('is_valid', sa.Boolean, default=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE"))
    )

    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE")),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow)
    )

    op.create_table(
        'goods',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('order_id', sa.Integer, sa.ForeignKey('orders.id', ondelete="CASCADE")),
        sa.Column('name', sa.String),
        sa.Column('count', sa.Integer),
        sa.Column('price', sa.Float)
    )

    users_table = table(
        'users',
        column('id', Integer),
        column('name', String),
        column('password_hash', String)
    )

    users_data = [
        {'id': 1, 'name': 'alice', 'password_hash': hashlib.md5('alicepass'.encode()).hexdigest()},
        {'id': 2, 'name': 'bob', 'password_hash': hashlib.md5('bobpass'.encode()).hexdigest()}
    ]

    op.bulk_insert(users_table, users_data)

    tokens_table = table(
        'tokens',
        column('id', Integer),
        column('value', String),
        column('is_valid', Boolean),
        column('user_id', Integer)
    )

    tokens_data = [
        {'id': 1, 'value': secrets.token_urlsafe(32), 'is_valid': True, 'user_id': 1},
        {'id': 2, 'value': secrets.token_urlsafe(32), 'is_valid': True, 'user_id': 2}
    ]

    op.bulk_insert(tokens_table, tokens_data)

    orders_table = table(
        'orders',
        column('id', Integer),
        column('user_id', Integer),
        column('created_at', DateTime)
    )

    orders_data = [
        {'id': 1, 'user_id': 1, 'created_at': datetime.utcnow()},
        {'id': 2, 'user_id': 1, 'created_at': datetime.utcnow()},
        {'id': 3, 'user_id': 2, 'created_at': datetime.utcnow()}
    ]

    op.bulk_insert(orders_table, orders_data)

    goods_table = table(
        'goods',
        column('id', Integer),
        column('order_id', Integer),
        column('name', String),
        column('count', Integer),
        column('price', Float)
    )

    goods_data = [
        {'id': 1, 'order_id': 1, 'name': 'apple', 'count': 3, 'price': 10.0},
        {'id': 2, 'order_id': 1, 'name': 'banana', 'count': 2, 'price': 5.0},
        {'id': 3, 'order_id': 2, 'name': 'milk', 'count': 1, 'price': 2.5},
        {'id': 4, 'order_id': 3, 'name': 'bread', 'count': 2, 'price': 3.0}
    ]

    op.bulk_insert(goods_table, goods_data)


def downgrade():
    op.drop_table('goods')
    op.drop_table('orders')
    op.drop_table('tokens')
    op.drop_table('users')