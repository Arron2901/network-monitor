from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import CheckResult


class CheckResultsRepository:
    """CRUD operations for MonitoredURL"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, url_id: int, response_time: int) -> CheckResult:
        site = CheckResult(
            url_id = url_id,
            response_time = response_time
        )
        self.session.add(site)
        await self.session.commit()
        await self.session.refresh(site)  # refresh to get id & defaults
        return site

    async def get_all(self) -> List[CheckResult]:
        result = await self.session.execute(select(CheckResult))
        return result.scalars().all()

    async def get_by_id(self, site_id: int) -> Optional[CheckResult]:
        return await self.session.get(CheckResult, site_id)

    async def update_response_time(self, site_id: int, response_time: int) -> None:
        stmt = (
            update(CheckResult)
            .where(CheckResult.id == site_id)
            .values(response_time = response_time)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, site_id: int) -> None:
        stmt = delete(CheckResult).where(CheckResult.id == site_id)
        await self.session.execute(stmt)
        await self.session.commit()
