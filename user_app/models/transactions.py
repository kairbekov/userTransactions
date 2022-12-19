import typing
from uuid import uuid4

import databases
import loguru
import sqlalchemy
from fastapi import HTTPException

from ..core.db import metadata
from ..schemas.transactions import TransactionsUpdate, TransactionsGet, StatusType
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
    ),
    sqlalchemy.Column(
        'created_date',
        sqlalchemy.TIMESTAMP(timezone=True),
        server_default=sqlalchemy.text('NOW()'),
        default=sqlalchemy.text('NOW()'),
        nullable=False,
    )
)


async def get_transaction(db: databases.Database, id: str) -> TransactionsGet:
    query = Transactions.select().where(Transactions.c.id == id)
    res = await db.fetch_one(query)
    if not res:
        raise HTTPException(status_code=404, detail=f'Transaction with id: {id} not found')
    return TransactionsGet(**res)


async def get_transactions(db: databases.Database) -> typing.List[TransactionsGet]:
    query = Transactions.select()
    res = await db.fetch_all(query)
    res = [TransactionsGet(**dict(t)) for t in res]
    return res


async def create_transaction(
        db: databases.Database,
        data: TransactionsGet
) -> TransactionsGet:
    data.id = str(uuid4())
    data.user_id = str(data.user_id)
    data = dict(data)
    query = Transactions.insert().values(**data).returning(Transactions.c.id)
    try:
        async with db.transaction():
            res = await db.execute(query)
            return await get_transaction(db, res)
    except Exception as e:
        loguru.logger.error(e)
        raise HTTPException(status_code=404, detail='Can not create new transaction')


async def update_transaction(
        db: databases.Database,
        id: str,
        data: TransactionsUpdate
) -> TransactionsGet:
    data.user_id = str(data.user_id)
    data = dict(data)
    query = Transactions.update().where(Transactions.c.id == id).values(
        **data).returning(Transactions.c.id)
    try:
        async with db.transaction():
            res = await db.execute(query)
            return await get_transaction(db, res)
    except Exception as e:
        loguru.logger.error(e)
        raise HTTPException(status_code=404, detail='Can not update this transaction')


async def delete_transaction(db: databases.Database, id: str):
    query = Transactions.delete().where(
        Transactions.c.id == id).returning(Transactions.c.id)
    try:
        async with db.transaction():
            res = await db.execute(query)
            return res
    except Exception as e:
        loguru.logger.error(e)
        raise HTTPException(status_code=404, detail='Can not delete this transaction')


async def get_all_user_transactions(db: databases.Database, user_id: str) -> typing.List[TransactionsGet]:
    query = 'Select t.* from transactions t where t.user_id = :user_id'
    res = await db.fetch_all(query, {'user_id': user_id})
    res = [TransactionsGet(**t) for t in res]
    return res


async def change_transaction_status(db: databases.Database, id: str, status: str):
    """
       If new status confirmed => then add to user balance
       If new status declined => do nothing
       If new status refund => create new transaction to return money to User
    """
    data = dict(await get_transaction(db, id))
    user = dict(await users.get_user(db, str(data.get('user_id'))))
    user_balance = 0

    if status == StatusType.confirmed and data.get('status') == StatusType.waiting:
        user_balance = data.get('amount')
    elif status == StatusType.declined and data.get('status') == StatusType.waiting:
        # notify user that Declined
        pass
    elif status == StatusType.refund and data.get('status') == StatusType.confirmed:
        user_balance = data.get('amount')
        if user_balance > user.get('balance', 0):
            raise HTTPException(status_code=404, detail='Cant refund, low balance')
        await create_transaction(db, TransactionsGet(
            status=status, user_id=data.get('user_id'), balance=user_balance))

    res = await update_transaction(db, id, TransactionsUpdate(status=status))
    user['balance'] = user.get('balance', 0) + user_balance
    user.pop('id')
    await users.update_user(db, data.get('user_id'), UserUpdate(**user))

    return res
