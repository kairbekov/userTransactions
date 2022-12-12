from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel


class User(BaseModel):
    id: Optional[UUID] = uuid4
    name: str
    surname: str
    balance: float
