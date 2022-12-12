from uuid import uuid4

import databases
import loguru
import sqlalchemy
from ..core.db import metadata
from ..schemas import transactions
from ..models import users
from ..schemas.users import UserUpdate

Transactions = sqlalchemy.Table(
    'transactions',
    metadata,
    sqlalchemy.Column(
        'id',
        sqlalchemy.Text,
        primary_key=True
    ),
    sqlalchemy.Column(
        'user_id',
        sqlalchemy.Text,
        sqlalchemy.ForeignKey('users.id'),
        nullable=False,
    ),
    sqlalchemy.Column(
        'transaction_type',
        sqlalchemy.Text,
        nullable=True,
    ),
    sqlalchemy.Column(
        'amount',
        sqlalchemy.Float,
        nullable=True,
    ),
    sqlalchemy.Column(
        'status',
        sqlalchemy.Text,
        nullable=True,
    )
)


async def get_transaction(db: databases.Database, id: str):
    query = Transactions.select().where(Transactions.c.id == id)
    res = await db.fetch_one(query)
    return res


async def get_transactions(db: databases.Database):
    query = Transactions.select()
    res = await db.fetch_all(query)
    return res


async def create_transaction(db: databases.Database, data: transactions.Transactions):
    data.id = str(uuid4())
    data.user_id = str(data.user_id)
    data = dict(data)
    query = Transactions.insert().values(**data).returning(Transactions.c.id)
    res = await db.execute(query)
    return res


async def update_transaction(
        db: databases.Database,
        id: str,
        data: transactions.TransactionsUpdate
):
    data.user_id = str(data.user_id)
    data = dict(data)
    query = Transactions.update().where(Transactions.c.id == id).values(
        **data).returning(Transactions.c.id)
    res = await db.fetch_one(query)
    return res


async def delete_transaction(db: databases.Database, id: str):
    query = Transactions.delete().where(
        Transactions.c.id == id).returning(Transactions.c.id)
    res = await db.fetch_one(query)
    return res


async def get_all_user_transactions(db: databases.Database, user_id: str):
    query = 'Select t.* from transactions t where t.user_id = :user_id'
    res = await db.fetch_one(query, {'user_id': user_id})
    return res


async def change_transaction_status(db: databases.Database, id: str, status: str):
    data = dict(await get_transaction(db, id))
    user = dict(await users.get_user(db, data.get('user_id')))
    user_balance = 0

    if status == transactions.StatusType.confirmed and data.get('status') != status:
        user_balance = data.get('amount')
    elif status == transactions.StatusType.declined and data.get('status') != status:
        user_balance = data.get('amount') * -1
    elif status == transactions.StatusType.refund and \
            data.get('status') == transactions.StatusType.confirmed:
        user_balance = data.get('amount')
        await create_transaction(db, transactions.Transactions(
            status=status, user_id=data.get('user_id'), balance=user_balance))
    res = await update_transaction(db, id, transactions.TransactionsUpdate(status=status))
    user['balance'] = user.get('balance', 0) + user_balance
    user.pop('id')
    await users.update_user(db, data.get('user_id'), UserUpdate(**user))

    return res
