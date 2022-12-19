import fastapi

from . import users
from . import transactions

router = fastapi.APIRouter()

router.include_router(users.router,  tags=['users'], prefix='/users',
                      responses={404: {'description': 'Not Found!'}})
router.include_router(transactions.router, tags=['transactions'],
                      prefix='/transactions',
                      responses={404: {'description': 'Not Found!'}})
