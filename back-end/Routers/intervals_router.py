from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel

from database import SessionLocal
from Classes.Intervals import IntervalsRepository

router = APIRouter(prefix="/intervals", tags=["Intervals"])

# Pydantic schemas
class IntervalsSchema(BaseModel):
    id: int
    url_id: int
    time_interval: int

    class Config:
        orm_mode = True

class IntervalsCreate(BaseModel):
    url_id: int
    time_interval: int

class IntervalUpdateTimeInterval(BaseModel):
    time_interval: int

# Dependency
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

# CREATE
@router.post('/create', response_model=IntervalsSchema)
async def create_interval(site: IntervalsCreate, session: AsyncSession = Depends(get_session)):
    repo = IntervalsRepository(session)
    db_site = await repo.create(site.url_id, site.time_interval)
    return db_site

# READ ALL
@router.get('/fetch_all', response_model=List[IntervalsSchema])
async def get_intervals(session: AsyncSession = Depends(get_session)):
    repo = IntervalsRepository(session)
    sites = await repo.get_all()
    return sites

# READ SPECIFIC
@router.get('/fetch_specific/{interval_id}', response_model=dict)
async def get_specific_intervals(interval_id: int, session: AsyncSession = Depends(get_session)):
    repo = IntervalsRepository(session)
    site = await repo.get_by_id(interval_id)
    if not site:
        raise HTTPException(status_code=404, detail='Interval not found')
    return site

# UPDATE INTERVAL
@router.patch('/update_time_interval/{interval_id}', response_model=IntervalsSchema)
async def update_time_interval(interval_id: int, interval: IntervalUpdateTimeInterval, session: AsyncSession = Depends(get_session)):
    repo = IntervalsRepository(session)
    site = await repo.get_by_id(interval_id)
    if not site:
        raise HTTPException(status_code=404, detail="Interval not found")
    await repo.update_interval(interval_id, interval.time_interval)
    updated_site = await repo.get_by_id(interval_id)
    return updated_site

# DELETE
@router.delete("/delete/{interval_id}", response_model=dict)
async def delete_interval(interval_id: int, session: AsyncSession = Depends(get_session)):
    repo = IntervalsRepository(session)
    site = await repo.get_by_id(interval_id)
    if not site:
        raise HTTPException(status_code=404, detail="Interval not found")
    await repo.delete(interval_id)
    return {"detail": "Interval deleted successfuly"}