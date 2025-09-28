import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import SessionLocal, engine
from models import Intervals
from Classes.Intervals import IntervalsRepository


@pytest_asyncio.fixture
async def session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
        await session.rollback()

@pytest.mark.asyncio
async def test_monitored_urls_repo(session):
    repo = IntervalsRepository(session)

    # CREATE
    site = await repo.create(1, 5)
    assert site.url_id == 1
    assert site.time_interval == 5

    # READ
    fetched_site = await repo.get_by_id(site.id)
    assert fetched_site.time_interval == 5

    # UPDATE
    await repo.update_interval(site.id, time_interval=1)
    updated_site = await repo.get_by_id(site.id)
    assert updated_site.time_interval == 1

    # DELETE
    await repo.delete(site.id)
    deleted_site = await repo.get_by_id(site.id)
    assert deleted_site is None
