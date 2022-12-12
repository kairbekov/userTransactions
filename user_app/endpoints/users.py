import databases
import loguru
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependecies import get_db, get_session
from .. import models

router = APIRouter()


@router.get('/users/', tags=["users"])
async def get_list(db: databases.Database = Depends(get_session)):
    loguru.logger.debug(f'ABL {db}')
    user_list = await models.users.get_users(db)
    return user_list


@router.get('/users/{id}', tags=["users"])
async def get(id):
    return {"username": f"user with id: {id}"}

