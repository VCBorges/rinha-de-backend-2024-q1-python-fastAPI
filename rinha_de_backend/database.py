from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

DB_USER = 'rinha_user'
DB_PASSWORD = '123qaz123'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'rinha_db'

DATABASE_URL = (
    f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

engine: AsyncEngine = create_async_engine(DATABASE_URL, future=True, echo=True)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
    )
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
