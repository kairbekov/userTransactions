import datetime
import typing
from enum import Enum
from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel


class TransactionType(str, Enum):
    direct = "direct"


class StatusType(str, Enum):
    waiting = "waiting"
    confirmed = "confirmed"
    declined = "declined"
    refund = "refund"


class TransactionsUpdate(BaseModel):
    user_id: typing.Optional[UUID]
    transaction_type: typing.Optional[TransactionType]
    amount: typing.Optional[float]
    status: typing.Optional[StatusType]


class TransactionsGet(TransactionsUpdate):
    id: Optional[UUID]
    created_date: datetime.datetime
