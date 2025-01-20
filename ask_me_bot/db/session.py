from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from config import settings


engine: AsyncEngine = create_async_engine(settings.get_db_url())


async def create_session():
    async with AsyncSession(engine) as session:
        return session
