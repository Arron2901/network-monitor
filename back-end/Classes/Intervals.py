from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import Intervals


class IntervalsRepository:
    """CRUD operations for Intervals"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, url_id: int, time_interval: int) -> Intervals:
        site = Intervals(
            url_id = url_id,
            time_interval = time_interval
        )
        self.session.add(site)
        await self.session.commit()
        await self.session.refresh(site)
        return site

    async def get_all(self) -> List[Intervals]:
        result = await self.session.execute(select(Intervals))
        return result.scalars().all()

    async def get_by_id(self, site_id: int) -> Optional[Intervals]:
        return await self.session.get(Intervals, site_id)

    async def update_interval(self, site_id: int, time_interval: int) -> None:
        stmt = (
            update(Intervals)
            .where(Intervals.id == site_id)
            .values(time_interval = time_interval)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, site_id: int) -> None:
        stmt = delete(Intervals).where(Intervals.id == site_id)
        await self.session.execute(stmt)
        await self.session.commit()
