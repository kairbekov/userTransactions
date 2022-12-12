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
    res = await models.transactions.get_transaction(db, id)
    return res


@router.post('/transactions/', tags=["transactions"])
async def create(data: schemas.transactions.Transactions,
                 db: databases.Database = Depends(get_session)):
    res = await models.transactions.create_transaction(db, data)
    return res


@router.put('/transactions/{id}', tags=["transactions"])
async def update(id: str, data: schemas.transactions.TransactionsUpdate,
                 db: databases.Database = Depends(get_session)):
    res = await models.transactions.update_transaction(db, id, data)
    return res


@router.delete('/transactions/{id}', tags=["transactions"])
async def delete(id: str, db: databases.Database = Depends(get_session)):
    res = await models.transactions.delete_transaction(db, id)
    return res


@router.get('/transactions/by_user/{id}', tags=["transactions"])
async def get_all_user_transactions(id: str, db: databases.Database = Depends(get_session)):
    res = await models.transactions.get_all_user_transactions(db, id)
    return res


@router.put('/transactions/change_status/{id}', tags=["transactions"])
async def change_transaction_status(id: str, status: str,
                                    db: databases.Database = Depends(get_session)):
    res = await models.transactions.change_transaction_status(db, id, status)
    return res
