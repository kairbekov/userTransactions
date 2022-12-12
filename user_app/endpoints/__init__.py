import fastapi

from . import users
from . import transactions

router = fastapi.APIRouter()

router.include_router(users.router)
router.include_router(transactions.router)
