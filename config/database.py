import logging

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from config.settings import settings

logger = logging.getLogger(__name__)

Base = declarative_base()


# Database URL for SQLAlchemy connection string
db_url = URL.create(
    drivername=settings.db_driver,
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)


class Database:
    def __init__(self):
        self.__session = None
        self.__engine = None

    def connect(self):
        self.__engine = create_async_engine(url=db_url)

        self.__session = async_sessionmaker(
            bind=self.__engine,
            autocommit=False,
        )

    async def disconnect(self):
        await self.__engine.dispose()

    async def get_db(self):
        async with db.__session() as session:
            yield session


db = Database()
