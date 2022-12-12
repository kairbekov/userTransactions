import typing

import databases
import loguru
import sqlalchemy


metadata = sqlalchemy.MetaData()

_SESSION: typing.Optional[databases.Database] = None

# URL = 'sqlite+aiosqlite:///./example.db'
URL = 'postgresql+asyncpg://user_app:user_app@localhost:5432/user_app'


class SessionNotInitializedError:
    """
    Session is not initialized yet!
    """
    pass


async def get_connected_session() -> databases.Database:
    res = databases.Database(URL)
    await res.connect()
    return res


async def connect() -> databases.Database:
    global _SESSION

    if _SESSION is None:
        _SESSION = await get_connected_session()

    return _SESSION


async def get_req_session():
    return get_session()


def get_session() -> databases.Database:
    global _SESSION

    if not _SESSION:
        raise SessionNotInitializedError

    return _SESSION


async def disconnect() -> None:
    global _SESSION

    if _SESSION is not None and _SESSION.is_connected:
        await _SESSION.disconnect()
        _SESSION = None
