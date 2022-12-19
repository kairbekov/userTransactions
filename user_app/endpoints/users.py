import typing

import databases

from fastapi import APIRouter, Depends, status

from .. import models, schemas
from ..dependecies import get_session

router = APIRouter()


@router.get(
    '/',
    response_model=typing.List[schemas.users.User],
    status_code=status.HTTP_200_OK,
    summary='Get List of all users',
)
async def get_list(db: databases.Database = Depends(get_session)):
    user_list = await models.users.get_users(db)
    return user_list


@router.get(
    '/{id}',
    response_model=schemas.users.User,
    status_code=status.HTTP_200_OK,
    summary='Get User by id',
)
async def get(id: str, db: databases.Database = Depends(get_session)):
    user = await models.users.get_user(db, id)
    return user


@router.post(
    '/',
    response_model=schemas.users.User,
    status_code=status.HTTP_200_OK,
    summary='Create New User',
)
async def create(
        data: schemas.users.User,
        db: databases.Database = Depends(get_session),
):
    user = await models.users.create_user(db, data)
    return user


@router.put(
    '/{id}',
    response_model=schemas.users.User,
    status_code=status.HTTP_200_OK,
    summary='Update User',
)
async def update(
        id: str,
        data: schemas.users.UserUpdate,
        db: databases.Database = Depends(get_session),
):
    user = await models.users.update_user(db, id, data)
    return user


@router.delete(
    '/{id}',
    status_code=status.HTTP_200_OK,
    summary='Delete User',
)
async def delete(id: str, db: databases.Database = Depends(get_session)):
    user = await models.users.delete_user(db, id)
    return user


@router.get(
    '/balance/{id}',
    response_model=schemas.users.UserBalance,
    status_code=status.HTTP_200_OK,
    summary='Get User balance',
)
async def get_user_balance(
        id: str,
        db: databases.Database = Depends(get_session),
):
    user = await models.users.get_user_balance(db, id)
    return user
