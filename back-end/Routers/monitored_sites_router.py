from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Annotated, Optional
import models
from database import SessionLocal
from sqlalchemy.orm import Session


# -------------------- Pydantic Schemas --------------------

class SiteStatusBase(BaseModel):
    """Schema for site status."""
    id: int
    status: bool

    class Config:
        orm_mode = True


class SiteIntervalBase(BaseModel):
    """Schema for site check intervals."""
    id: int
    time_interval: int

    class Config:
        orm_mode = True


class MonitoredSitesBase(BaseModel):
    """Base schema for monitored sites."""
    id: int
    site_url: str
    site_name: str

    # Add relationships
    intervals: List[SiteIntervalBase] = []
    statuses: List[SiteStatusBase] = []

    class Config:
        orm_mode = True


class MonitoredSitesCreate(BaseModel):
    site_url: str
    site_name: str


class MonitoredSitesUpdate(BaseModel):
    site_url: Optional[str] = None
    site_name: Optional[str] = None


# -------------------- DB Dependency --------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

# -------------------- Router --------------------

router = APIRouter(prefix="/monitored_sites", tags=["Monitored Sites"])


@router.post("/create", response_model=MonitoredSitesBase)
async def create_monitored_site(site: MonitoredSitesCreate, db: db_dependency):
    db_site = models.MonitoredSites(site_url=site.site_url, site_name=site.site_name)
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site


@router.get("/fetch", response_model=List[MonitoredSitesBase])
async def fetch_sites(db: db_dependency, site_id: Optional[int] = Query(default=None)):
    """
    Fetch monitored sites with intervals + statuses included.
    """
    query = db.query(models.MonitoredSites)

    if site_id:
        site = query.filter(models.MonitoredSites.id == site_id).first()
        if not site:
            raise HTTPException(status_code=404, detail="Unable to find specified site")
        return [site]  # still return a list for consistent shape

    return query.all()


@router.patch("/update", response_model=MonitoredSitesBase)
async def update_site(db: db_dependency, site_id: int, site_update: MonitoredSitesUpdate):
    site = db.query(models.MonitoredSites).filter(models.MonitoredSites.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Unable to find specified site")
    
    update_data = site_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(site, key, value)
    
    db.commit()
    db.refresh(site)
    return site


@router.delete("/delete")
async def delete_site(site_id: int, db: db_dependency):
    site = db.query(models.MonitoredSites).filter(models.MonitoredSites.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Unable to find specified site")

    db.delete(site)
    db.commit()

    return {"message": "Successfully deleted site"}
