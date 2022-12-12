from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel


class UserUpdate(BaseModel):
    name: str
    surname: str
    balance: float


class User(UserUpdate):
    id: Optional[UUID]
