from sqlalchemy.ext.asyncio import AsyncSession

from .core.database import SessionLocal, async_session
from .core.db import get_req_session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# async def get_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session


async def get_session():
    return await get_req_session()
