import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv('.envs/dev/db.env')

print(os.environ['DB_USER'])

DATABASE_URI: str = f"postgresql+psycopg2://{os.environ['DB_USER']}:" \
                    f"{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:" \
                    f"{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"


class DataBaseEngine:
    _base_engine = None

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.getLevelName(os.environ['LOG_LEVEL']))

    def __new__(cls):
        if cls._base_engine is None:
            cls._base_engine = create_engine(DATABASE_URI, pool_size=10, max_overflow=20)

        return cls._base_engine
