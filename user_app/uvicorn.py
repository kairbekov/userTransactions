import uvicorn


def run():
    uvicorn.run(
        "user_app:app",
        host='localhost',
        port=8000,
        loop="none",
        access_log=True,
        date_header=True,
        use_colors=True,
        forwarded_allow_ips='*',
        proxy_headers=True,
        reload_delay=1.0,
        workers=1,
    )
