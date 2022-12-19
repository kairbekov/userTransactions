import typing
from uuid import uuid4
import databases
import loguru
import sqlalchemy

from fastapi import HTTPException

from ..core.db import metadata
from ..schemas import users

User = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column(
        'id',
        sqlalchemy.Text,
        primary_key=True,
    ),
    sqlalchemy.Column(
        'name',
        sqlalchemy.Text,
        nullable=True,
    ),
    sqlalchemy.Column(
        'surname',
        sqlalchemy.Text,
        nullable=True,
    ),
    sqlalchemy.Column(
        'balance',
        sqlalchemy.Float(),
        nullable=True,
    ),
)


async def get_user(db: databases.Database, user_id: str) -> users.User:
    query = User.select().where(User.c.id == user_id)
    res = await db.fetch_one(query)
    if not res:
        raise HTTPException(status_code=404, detail=f'User with id: {user_id} not found')
    return users.User(**res)


async def get_users(db: databases.Database) -> typing.List[users.User]:
    query = User.select()
    res = await db.fetch_all(query)
    res = [users.User(**u) for u in res]
    return res


async def create_user(db: databases.Database, user: users.User) -> users.User:
    user.id = str(uuid4())
    user = dict(user)
    query = User.insert().values(**user).returning(User.c.id)
    try:
        async with db.transaction():
            res = await db.execute(query)
            return await get_user(db, res)
    except Exception as e:
        loguru.logger.error(e)
        raise HTTPException(status_code=404, detail='Can not create new user')


async def update_user(
        db: databases.Database,
        user_id: str,
        data: users.UserUpdate,
) -> users.User:
    data = dict(data)
    query = User.update().where(User.c.id == user_id).values(**data).returning(User.c.id)
    try:
        async with db.transaction():
            res = await db.execute(query)
            return await get_user(db, res)
    except Exception as e:
        loguru.logger.error(e)
        raise HTTPException(status_code=404, detail='Can not update this user')


async def delete_user(db: databases.Database, user_id: str):
    query = User.delete().where(User.c.id == user_id).returning(User.c.id)
    try:
        async with db.transaction():
            res = await db.execute(query)
            return res
    except Exception as e:
        loguru.logger.error(e)
        raise HTTPException(status_code=404, detail='Can not delete this user')


async def get_user_balance(
        db: databases.Database, user_id: str,
) -> users.UserBalance:
    # query = User.select(User.columns.balance).where(User.c.id == user_id)
    query = 'Select u.balance from users u where u.id = :user_id'
    res = await db.fetch_one(query, {'user_id': user_id})
    if not res:
        raise HTTPException(status_code=404, detail=f'User with id: {user_id} not found')
    return users.UserBalance(**res)
