import logging

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from config.settings import settings

logger = logging.getLogger(__name__)


## Database URL for SQLAlchemy connection string
db_url = URL.create(
    drivername=settings.db_driver,
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
).render_as_string(hide_password=False)

# Create an asynchronous engine instance
engine = create_async_engine(url=db_url, echo=True, future=True)


async def init_db():
    # Begin a new database session
    async with engine.begin() as conn:
        # Create all tables in the database which are defined by SQLModel's metadata
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    # Create a new asynchronous session
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    # Yield the session and close it after use
    async with async_session() as session:
        yield session


async def disconnect_db():
    # Close the connection pool
    await engine.dispose()


async def commit_rollback(session: AsyncSession):
    try:
        await session.commit()
        logger.info("Committing transaction")
    except Exception:
        await session.rollback()
        raise
