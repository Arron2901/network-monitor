# routers/monitored_sites.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel

from database import SessionLocal
from Classes.CheckResults import CheckResultsRepository

router = APIRouter(prefix="/check_result", tags=["Check Results"])

# Pydantic schemas
class CheckResultSchema(BaseModel):
    id: int
    url_id: int
    response_time: int

    class Config:
        orm_mode = True

class CheckResultsCreate(BaseModel):
    url_id: int
    response_time: int

class CheckResultsUpdateReponseTime(BaseModel):
    response_time: int

# Dependency
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

# CREATE
@router.post("/create", response_model=CheckResultSchema)
async def create_site(site: CheckResultsCreate, session: AsyncSession = Depends(get_session)):
    repo = CheckResultsRepository(session)
    db_site = await repo.create(site.url_id, site.response_time)
    return db_site

# READ ALL
@router.get("/fetch_all", response_model=List[CheckResultSchema])
async def get_sites(session: AsyncSession = Depends(get_session)):
    repo = CheckResultsRepository(session)
    sites = await repo.get_all()
    return sites

# READ SPECIFIC
@router.get('/fetch_specific/{check_results_id}', response_model=dict)
async def get_specific_intervals(check_results_id: int, session: AsyncSession = Depends(get_session)):
    repo = CheckResultsRepository(session)
    site = await repo.get_by_id(check_results_id)
    if not site:
        raise HTTPException(status_code=404, detail='Interval not found')
    return site

# UPDATE STATUS
@router.patch("/update_response_time/{check_results_id}", response_model=CheckResultSchema)
async def update_site_status(check_results_id: int, time: CheckResultsUpdateReponseTime, session: AsyncSession = Depends(get_session)):
    repo = CheckResultsRepository(session)
    site = await repo.get_by_id(check_results_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    await repo.update_response_time(check_results_id, time.response_time)
    updated_site = await repo.get_by_id(check_results_id)
    return updated_site

# DELETE
@router.delete("/delete/{check_results_id}", response_model=dict)
async def delete_site(check_results_id: int, session: AsyncSession = Depends(get_session)):
    repo = CheckResultsRepository(session)
    site = await repo.get_by_id(check_results_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    await repo.delete(check_results_id)
    return {"detail": "Site deleted successfully"}
