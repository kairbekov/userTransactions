from sqlalchemy.ext.asyncio import AsyncSession

from .core.db import get_req_session


async def get_session():
    return await get_req_session()
