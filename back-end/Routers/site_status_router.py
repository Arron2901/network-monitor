from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Annotated, Optional
import models
from database import SessionLocal
from sqlalchemy.orm import Session


class SiteStatusBase(BaseModel):
    """Base schema for site status.

    Attributes:
        id (int): Unique identifier for the site status.
        site_url_id (int): Foreign key referencing the monitored site.
        status (bool): Current status of the site (True = up, False = down).
    """
    id: int
    site_url_id: int
    status: bool


class SiteStatusCreate(BaseModel):
    """Schema for creating a new site status.

    Attributes:
        site_url_id (int): Foreign key referencing the monitored site.
        status (bool): Current status of the site.
    """
    site_url_id: int
    status: bool


class SiteStatusUpdate(BaseModel):
    """Schema for updating a site status.

    Attributes:
        site_url_id (Optional[int]): Foreign key referencing the monitored site.
        status (Optional[bool]): Current status of the site.
    """
    site_url_id: Optional[int] = None
    status: Optional[bool] = None


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

# Create a router for site status
router = APIRouter(prefix="/site_status", tags=["Site Status"])


@router.post("/create", response_model=SiteStatusBase)
async def create_site_status(status: SiteStatusCreate, db: db_dependency):
    """Create a new site status.

    Args:
        status (SiteStatusCreate): The site status data to create.
        db (Session): The database session dependency.

    Returns:
        SiteStatusBase: The created site status.

    Raises:
        HTTPException: If a database error occurs during commit.
    """
    db_status = models.SiteStatus(
        site_url_id=status.site_url_id,
        status=status.status
    )
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status


@router.get("/fetch", response_model=List[SiteStatusBase])
async def fetch_site_statuses(db: db_dependency, status_id: Optional[int] = Query(default=None)):
    """Fetch site statuses.

    Args:
        db (Session): The database session dependency.
        status_id (Optional[int], optional): ID of a specific status to fetch.
            If not provided, all statuses are returned. Defaults to None.

    Returns:
        List[SiteStatusBase]: A list of statuses if no status_id is provided.
        SiteStatusBase: A single status if status_id is provided.

    Raises:
        HTTPException: If a status with the given ID is not found (404).
    """
    if status_id is None:
        return db.query(models.SiteStatus).all()

    result = db.query(models.SiteStatus).filter(models.SiteStatus.id == status_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Unable to find specified status")
    
    return result


@router.patch("/update", response_model=SiteStatusBase)
async def update_site_status(
    status_id: int, status_update: SiteStatusUpdate, db: db_dependency
):
    """Update a site status.

    Args:
        status_id (int): ID of the status to update.
        status_update (SiteStatusUpdate): Fields to update.
        db (Session): The database session dependency.

    Returns:
        SiteStatusBase: The updated site status.

    Raises:
        HTTPException: If a status with the given ID is not found (404).
    """
    status = db.query(models.SiteStatus).filter(models.SiteStatus.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Unable to find specified status")
    
    update_data = status_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(status, key, value)
    
    db.commit()
    db.refresh(status)
    return status


@router.delete("/delete")
async def delete_site_status(status_id: int, db: db_dependency):
    """Delete a site status by ID.

    Args:
        status_id (int): ID of the status to delete.
        db (Session): The database session dependency.

    Returns:
        str: Success message.

    Raises:
        HTTPException: If a status with the given ID is not found (404).
    """
    status = db.query(models.SiteStatus).filter(models.SiteStatus.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Unable to find specified status")

    db.delete(status)
    db.commit()

    return "Successfully deleted status"
