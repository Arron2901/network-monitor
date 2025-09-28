import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import SessionLocal, engine
from models import MonitoredURL
from Classes.MonitoredURLS import MonitoredURLRepository

@pytest_asyncio.fixture
async def session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
        await session.rollback()

@pytest.mark.asyncio
async def test_monitored_urls_repo(session):
    repo = MonitoredURLRepository(session)

    # CREATE
    site = await repo.create("Example", "https://example.com", is_up=True)
    assert site.name == "Example"
    assert site.is_up is True

    # READ
    fetched_site = await repo.get_by_id(site.id)
    assert fetched_site.name == "Example"

    # UPDATE
    await repo.update_status(site.id, is_up=False)
    updated_site = await repo.get_by_id(site.id)
    assert updated_site.is_up is False
    assert updated_site.last_checked is not None

    # DELETE
    await repo.delete(site.id)
    deleted_site = await repo.get_by_id(site.id)
    assert deleted_site is None
