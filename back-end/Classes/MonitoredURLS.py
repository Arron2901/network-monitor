from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import MonitoredURL


class MonitoredURLRepository:
    """CRUD operations for MonitoredURL"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str, url: str, is_up: bool = False) -> MonitoredURL:
        site = MonitoredURL(
            name=name,
            url=url,
            is_up=is_up,
        )
        self.session.add(site)
        await self.session.commit()
        await self.session.refresh(site)  # refresh to get id & defaults
        return site

    async def get_all(self) -> List[MonitoredURL]:
        result = await self.session.execute(select(MonitoredURL))
        return result.scalars().all()

    async def get_by_id(self, site_id: int) -> Optional[MonitoredURL]:
        return await self.session.get(MonitoredURL, site_id)

    async def update_status(self, site_id: int, is_up: bool) -> None:
        stmt = (
            update(MonitoredURL)
            .where(MonitoredURL.id == site_id)
            .values(is_up=is_up, last_checked=datetime.utcnow())
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, site_id: int) -> None:
        stmt = delete(MonitoredURL).where(MonitoredURL.id == site_id)
        await self.session.execute(stmt)
        await self.session.commit()
