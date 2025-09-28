import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import SessionLocal, engine
from models import Intervals
from Classes.CheckResults import CheckResultsRepository


@pytest_asyncio.fixture
async def session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
        await session.rollback()

@pytest.mark.asyncio
async def test_monitored_urls_repo(session):
    repo = CheckResultsRepository(session)

    # CREATE
    site = await repo.create(1, 10)
    assert site.url_id == 1
    assert site.response_time == 10

    # READ
    fetched_site = await repo.get_by_id(site.id)
    assert fetched_site.response_time == 10

    # UPDATE
    await repo.update_response_time(site.id, response_time=20)
    updated_site = await repo.get_by_id(site.id)
    assert updated_site.response_time == 20

    # DELETE
    await repo.delete(site.id)
    deleted_site = await repo.get_by_id(site.id)
    assert deleted_site is None
