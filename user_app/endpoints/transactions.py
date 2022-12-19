import typing

import databases
from fastapi import APIRouter, Depends, status
from ..dependecies import get_session
from .. import models, schemas

router = APIRouter()


@router.get(
    '/',
    response_model=typing.List[schemas.transactions.TransactionsGet],
    status_code=status.HTTP_200_OK,
    summary='Get List of all transactions'
)
async def get_transactions(db: databases.Database = Depends(get_session)):
    transactions_list = await models.transactions.get_transactions(db)
    return transactions_list


@router.get(
    '/{id}',
    response_model=schemas.transactions.TransactionsGet,
    status_code=status.HTTP_200_OK,
    summary='Get Transactions by ID'
)
async def get_transaction(id: str, db: databases.Database = Depends(get_session)):
    res = await models.transactions.get_transaction(db, id)
    return res


@router.post(
    '/',
    response_model=schemas.transactions.TransactionsGet,
    status_code=status.HTTP_200_OK,
    summary='Create transaction'
)
async def create(data: schemas.transactions.TransactionsGet,
                 db: databases.Database = Depends(get_session)):
    res = await models.transactions.create_transaction(db, data)
    return res


@router.put(
    '/{id}',
    response_model=schemas.transactions.TransactionsGet,
    status_code=status.HTTP_200_OK,
    summary='Update transaction'
)
async def update(id: str, data: schemas.transactions.TransactionsUpdate,
                 db: databases.Database = Depends(get_session)):
    res = await models.transactions.update_transaction(db, id, data)
    return res


@router.delete(
    '/{id}',
    status_code=status.HTTP_200_OK,
    summary='Delete transaction'
)
async def delete(id: str, db: databases.Database = Depends(get_session)):
    res = await models.transactions.delete_transaction(db, id)
    return res


@router.get(
    '/by_user/{id}',
    response_model=typing.List[schemas.transactions.TransactionsGet],
    status_code=status.HTTP_200_OK,
    summary='Get List of all transactions of user'
)
async def get_all_user_transactions(id: str, db: databases.Database = Depends(get_session)):
    res = await models.transactions.get_all_user_transactions(db, id)
    return res


@router.put(
    '/change_status/{id}',
    status_code=status.HTTP_200_OK,
    summary='Change transaction status'
)
async def change_transaction_status(id: str, status: schemas.transactions.StatusType,
                                    db: databases.Database = Depends(get_session)):
    res = await models.transactions.change_transaction_status(db, id, status)
    return res
