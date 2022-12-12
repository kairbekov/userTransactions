import databases
import loguru
from fastapi import APIRouter, Depends
from ..dependecies import get_db, get_session
from .. import models, schemas

router = APIRouter()


@router.get('/users/', tags=["users"])
async def get_list(db: databases.Database = Depends(get_session)):
    user_list = await models.users.get_users(db)
    return user_list


@router.get('/users/{id}', tags=["users"])
async def get(id: str, db: databases.Database = Depends(get_session)):
    user = await models.users.get_user(db, id)
    return user


@router.post('/users/', tags=["users"])
async def create(data: schemas.users.User, db: databases.Database = Depends(get_session)):
    user = await models.users.create_user(db, data)
    return user


@router.put('/users/{id}', tags=["users"])
async def update(id: str, data: schemas.users.UserUpdate, db: databases.Database = Depends(get_session)):
    user = await models.users.update_user(db, id, data)
    return user


@router.delete('/users/{id}', tags=["users"])
async def delete(id: str, db: databases.Database = Depends(get_session)):
    user = await models.users.delete_user(db, id)
    return user


@router.get('/users/balance/{id}', tags=["users"])
async def get_user_balance(id: str, db: databases.Database = Depends(get_session)):
    user = await models.users.get_user_balance(db, id)
    return user
