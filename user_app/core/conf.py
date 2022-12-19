import confboy


_base_config = {
    'log_level': 'DEBUG',
    'debug': True,
    'workers': 2,
    'api': {
        'port': 8000,
        'host': '0.0.0.0',
        'ssl': True
    },
    'db': {
        'host': 'db',
        # 'host': '0.0.0.0',
        'port': 5432,
        'username': 'user_app',
        'password': 'user_app',
        'database': 'user_app',
        'connection_count': 16
    },
    'postgres_url': 'callable:_build_postgres_url',
}


conf = confboy.Config(_base_config)


def _build_postgres_url():
    c = conf.db
    cnt = c.connection_count or 4
    return f'postgresql://{c.username}:{c.password}@{c.host}:{c.port}/{c.database}?min_size={cnt}&max_size={cnt}'


conf.register_callable(_build_postgres_url)
