import uvicorn

from .core import conf


def run():
    uvicorn.run(
        'user_app:app',
        host=conf.conf.api.host,
        port=conf.conf.api.port,
        log_level=conf.conf.log_level.lower(),
        loop='none',
        debug=conf.conf.debug,
        access_log=True,
        date_header=True,
        use_colors=True,
        forwarded_allow_ips='*',
        proxy_headers=True,
        reload_delay=1.0,
        workers=conf.conf.workers,
    )
