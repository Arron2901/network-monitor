from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Annotated, Optional
import models
from database import SessionLocal
from sqlalchemy.orm import Session


class MonitoredSitesBase(BaseModel):
    """Base schema for monitored sites.

    Attributes:
        id (int): Unique identifier for the monitored site.
        site_url (str): The URL of the monitored site.
        site_name (str): The name of the monitored site.
    """
    id: int
    site_url: str
    site_name: str


class MonitoredSitesCreate(BaseModel):
    """Schema for creating a monitored site.

    Attributes:
        site_url (str): The URL of the monitored site to create.
        site_name (str): The name of the monitored site to create.
    """
    site_url: str
    site_name: str


class MonitoredSitesUpdate(BaseModel):
    """Schema for updating a monitored site.

    Attributes:
        site_url (Optional[str]): The new URL of the monitored site.
        site_name (Optional[str]): The new name of the monitored site.
    """
    site_url: Optional[str] = None
    site_name: Optional[str] = None


def get_db():
    """Provide a database session dependency.

    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency injection type alias
db_dependency = Annotated[Session, Depends(get_db)]

# Create a router for monitored sites
router = APIRouter(prefix="/monitored_sites", tags=["Monitored Sites"])


@router.post("/create", response_model=MonitoredSitesBase)
async def create_monitored_site(site: MonitoredSitesCreate, db: db_dependency):
    """Create a new monitored site.

    Args:
        site (MonitoredSitesCreate): The monitored site data to create.
        db (Session): The database session dependency.

    Returns:
        MonitoredSitesBase: The created monitored site.

    Raises:
        HTTPException: If a database error occurs during commit.
    """
    db_site = models.MonitoredSites(site_url=site.site_url, site_name=site.site_name)
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site


@router.get("/fetch", response_model=List[MonitoredSitesBase])
async def fetch_sites(db: db_dependency, site_id: Optional[int] = Query(default=None)):
    """Fetch monitored sites.

    Args:
        db (Session): The database session dependency.
        site_id (Optional[int], optional): ID of a specific site to fetch.
            If not provided, all monitored sites are returned. Defaults to None.

    Returns:
        List[MonitoredSitesBase]: A list of monitored sites if no site_id is provided.
        MonitoredSitesBase: A single monitored site if site_id is provided.

    Raises:
        HTTPException: If a monitored site with the given ID is not found (404).
    """
    if site_id is None:
        return db.query(models.MonitoredSites).all()

    result = db.query(models.MonitoredSites).filter(models.MonitoredSites.id == site_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Unable to find specified site")
    
    return result


@router.patch("/update", response_model=MonitoredSitesBase)
async def update_site(db: db_dependency, site_id: int, site_update: MonitoredSitesUpdate):
    """Update a monitored site.

    Args:
        db (Session): The database session dependency.
        site_id (int): ID of the site to update.
        site_update (MonitoredSitesUpdate): Fields to update.

    Returns:
        MonitoredSitesBase: The updated monitored site.

    Raises:
        HTTPException: If a monitored site with the given ID is not found (404).
    """
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
    """Delete a monitored site by ID.

    Args:
        site_id (int): ID of the site to delete.
        db (Session): The database session dependency.

    Returns:
        str: Success message.

    Raises:
        HTTPException: If a monitored site with the given ID is not found (404).
    """
    site = db.query(models.MonitoredSites).filter(models.MonitoredSites.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Unable to find specified site")

    db.delete(site)
    db.commit()

    return "Successfully deleted site"
