from config.secret import *


class Settings:
    postgres_db = POSTGRES_URL
    alembic_db = ALEMBIC_DATABASE
    # data for entrance to postgres
    postgres_data = {
        "user": POSTGRES_USER,
        "password": POSTGRES_PASSWORD,
        "database": POSTGRES_DATABASE,
        "host": POSTGRES_HOST,
        "port": POSTGRES_PORT,
    }


