import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from wayweaver.db.session import AsyncSessionFactory


async def check_session_factory() -> None:
    async with AsyncSessionFactory() as session:
        assert isinstance(session, AsyncSession)


def test_session_factory_creates_async_session() -> None:
    asyncio.run(check_session_factory())