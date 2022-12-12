import fastapi
from fastapi.middleware.cors import CORSMiddleware

from .endpoints import router
from .core import db
_app = None


def create_app():
    global _app
    if _app is not None:
        return _app

    _app = fastapi.FastAPI(
        name='Traffic Analysing',
        docs_url='/api/docs',
        redoc_url='/api/redoc',
        openapi_url='/api/openapi.json',
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            '*',
            'http://localhost:3000',
            'http://localhost:8001',
            'http://localhost:7007',
        ],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    _app.include_router(
        router,
        prefix='/api/v1',
    )

    @_app.on_event('startup')
    async def on_start():
        await db.connect()
        pass

    @_app.on_event('shutdown')
    async def on_stop():
        await db.disconnect()
        pass

    return _app
