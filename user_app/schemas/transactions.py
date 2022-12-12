from enum import Enum
from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel


class TransactionType(str, Enum):
    direct = "direct"


class StatusType(str, Enum):
    confirmed = "confirmed"
    declined = "declined"
    refund = "refund"


class TransactionsUpdate(BaseModel):
    user_id: UUID
    transaction_type: TransactionType
    amount: float
    status: StatusType


class Transactions(TransactionsUpdate):
    id: Optional[UUID]
