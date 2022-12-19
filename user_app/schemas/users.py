from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel


class UserBalance(BaseModel):
    balance: float


class UserUpdate(UserBalance):
    name: Optional[str]
    surname: Optional[str]


class User(UserUpdate):
    id: Optional[UUID]
