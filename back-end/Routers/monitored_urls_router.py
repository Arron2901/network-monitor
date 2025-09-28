# routers/monitored_sites.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel

from database import SessionLocal
from Classes.MonitoredURLS import MonitoredURLRepository

router = APIRouter(prefix="/monitored_urls", tags=["Monitored Sites"])

# Pydantic schemas
class MonitoredURLSchema(BaseModel):
    id: int
    name: str
    url: str
    is_up: bool

    class Config:
        orm_mode = True

class MonitoredURLCreate(BaseModel):
    name: str
    url: str
    is_up: bool = False

class MonitoredURLUpdateStatus(BaseModel):
    is_up: bool

# Dependency
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

# CREATE
@router.post("/create", response_model=MonitoredURLSchema)
async def create_site(site: MonitoredURLCreate, session: AsyncSession = Depends(get_session)):
    repo = MonitoredURLRepository(session)
    db_site = await repo.create(site.name, site.url, site.is_up)
    return db_site

# READ ALL
@router.get("/fetch_all", response_model=List[MonitoredURLSchema])
async def get_sites(session: AsyncSession = Depends(get_session)):
    repo = MonitoredURLRepository(session)
    sites = await repo.get_all()
    return sites

# UPDATE STATUS
@router.patch("/update_status/{site_id}", response_model=MonitoredURLSchema)
async def update_site_status(site_id: int, status: MonitoredURLUpdateStatus, session: AsyncSession = Depends(get_session)):
    repo = MonitoredURLRepository(session)
    site = await repo.get_by_id(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    await repo.update_status(site_id, status.is_up)
    updated_site = await repo.get_by_id(site_id)
    return updated_site

# DELETE
@router.delete("/delete/{site_id}", response_model=dict)
async def delete_site(site_id: int, session: AsyncSession = Depends(get_session)):
    repo = MonitoredURLRepository(session)
    site = await repo.get_by_id(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    await repo.delete(site_id)
    return {"detail": "Site deleted successfully"}
