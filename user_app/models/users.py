import loguru
import sqlalchemy
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import relationship

from ..core.database import Base
from ..schemas import users as user_schema
from ..core.db import metadata
from ..core import db
from databases import Database


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


# def get_user(db: Session, user_id: int):
#     return db.query(User).filter(User.id == user_id).first()
#
#
# def get_user_by_email(db: Session, email: str):
#     return db.query(User).filter(User.email == email).first()


async def get_users(db):
    loguru.logger.debug(f'ABL {db}')
    res = await db.fetch_all(f'''select * from users''')
    # res = dict(res)
    loguru.logger.debug(f'ABL {res}')
    # res = [dict(item) for item in res]
    return {'res': res}
    # return db.query(User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: user_schema.UserCreate):
#     db_user = User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
