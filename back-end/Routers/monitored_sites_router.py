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
    """
    id: int
    site_url: str


class MonitoredSitesCreate(BaseModel):
    """Schema for creating a monitored site.

    Attributes:
        site_url (str): The URL of the monitored site to create.
    """
    site_url: str 


class MonitoredSitesUpdateSiteURL(BaseModel):
    """Schema for updating a monitored site's URL.

    Attributes:
        site_url (str): The new URL of the monitored site.
    """
    site_url: str


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
    db_site = models.MonitoredSites(site_url=site.site_url)
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
        Union[List[MonitoredSitesBase], MonitoredSitesBase]:
            - A list of monitored sites if no site_id is provided.
            - A single monitored site if site_id is provided.

    Raises:
        HTTPException: If a monitored site with the given ID is not found (404).
    """
    if site_id is None:
        return db.query(models.MonitoredSites).all()

    result = db.query(models.MonitoredSites).filter(models.MonitoredSites.id == site_id).first()

    if not result:
        raise HTTPException(status_code=404, detail="Unable to find specified site")
    
    return result
