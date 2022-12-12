import databases
from fastapi import APIRouter, Depends
from ..dependecies import get_db, get_session
from .. import models, schemas

router = APIRouter()


@router.get('/transactions/', tags=["transactions"])
async def get_transactions(db: databases.Database = Depends(get_session)):
    transactions_list = await models.transactions.get_transactions(db)
    return transactions_list


@router.get('/transactions/{id}', tags=["transactions"])
async def get_transaction(id: str, db: databases.Database = Depends(get_session)):
    user = await models.transactions.get_transaction(db, id)
    return user


@router.post('/transactions/', tags=["transactions"])
async def create(data: schemas.transactions.Transactions,
                 db: databases.Database = Depends(get_session)):
    user = await models.transactions.create_transaction(db, data)
    return user


@router.put('/transactions/{id}', tags=["transactions"])
async def update(id: str, data: schemas.transactions.TransactionsUpdate,
                 db: databases.Database = Depends(get_session)):
    user = await models.transactions.update_transaction(db, id, data)
    return user


@router.delete('/transactions/{id}', tags=["transactions"])
async def delete(id: str, db: databases.Database = Depends(get_session)):
    user = await models.transactions.delete_transaction(db, id)
    return user


@router.get('/transactions/by_user/{id}', tags=["transactions"])
async def get_all_user_transactions(id: str, db: databases.Database = Depends(get_session)):
    user = await models.transactions.get_all_user_transactions(db, id)
    return user
