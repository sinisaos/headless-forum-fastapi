from piccolo.engine.postgres import PostgresEngine

from config import settings

DB = PostgresEngine(
    config={
        "database": settings.db_test_name,
        "user": settings.db_user,
        "password": settings.db_password,
        "host": settings.db_host,
        "port": settings.db_port,
    },
)
