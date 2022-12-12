from uuid import uuid4

import databases
import loguru
import sqlalchemy
from ..core.db import metadata
from ..schemas import users

User = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column(
        'id',
        sqlalchemy.Text,
        primary_key=True
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
    )
)


async def get_user(db: databases.Database, user_id: str):
    query = User.select().where(User.c.id == user_id)
    res = await db.fetch_one(query)
    return res


async def get_users(db: databases.Database):
    query = User.select()
    res = await db.fetch_all(query)
    return {'res': res}


async def create_user(db: databases.Database, user: users.User):
    user.id = str(uuid4())
    user = dict(user)
    query = User.insert().values(**user).returning(User.c.id)
    res = await db.execute(query)
    return res


async def update_user(db: databases.Database, user_id: str, data: users.UserUpdate):
    data = dict(data)
    query = User.update().where(User.c.id == user_id).values(**data).returning(User.c.id)
    res = await db.fetch_one(query)
    return res


async def delete_user(db: databases.Database, user_id: str):
    query = User.delete().where(User.c.id == user_id).returning(User.c.id)
    res = await db.fetch_one(query)
    return res


async def get_user_balance(db: databases.Database, user_id: str):
    # query = User.select(User.columns.balance).where(User.c.id == user_id)
    query = 'Select u.balance from users u where u.id = :user_id'
    res = await db.fetch_one(query, {'user_id': user_id})
    return res
