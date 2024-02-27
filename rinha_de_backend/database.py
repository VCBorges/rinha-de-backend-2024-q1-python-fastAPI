from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

DATABASE_URL = 'sqlite+aiosqlite:///example.db'

engine: AsyncEngine = create_async_engine(DATABASE_URL, future=True, echo=True)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(engine)
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e