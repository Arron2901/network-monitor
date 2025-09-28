from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Annotated, Optional
import models
from database import SessionLocal
from sqlalchemy.orm import Session


class SiteCheckIntervalsBase(BaseModel):
    """Base schema for site check intervals.

    Attributes:
        id (int): Unique identifier for the interval.
        site_url_id (int): Foreign key referencing the monitored site.
        time_interval (int): Time interval in hours for checking the site.
    """
    id: int
    site_url_id: int
    time_interval: int


class SiteCheckIntervalsCreate(BaseModel):
    """Schema for creating a new site check interval.

    Attributes:
        site_url_id (int): Foreign key referencing the monitored site.
        time_interval (int): Time interval in hours for checking the site.
    """
    site_url_id: int
    time_interval: int


class SiteCheckIntervalsUpdate(BaseModel):
    """Schema for updating a site check interval.

    Attributes:
        site_url_id (Optional[int]): Foreign key referencing the monitored site.
        time_interval (Optional[int]): Time interval in hours for checking the site.
    """
    site_url_id: Optional[int] = None
    time_interval: Optional[int] = None


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

# Create a router for site check intervals
router = APIRouter(prefix="/site_check_intervals", tags=["Site Check Intervals"])


@router.post("/create", response_model=SiteCheckIntervalsBase)
async def create_site_check_interval(interval: SiteCheckIntervalsCreate, db: db_dependency):
    """Create a new site check interval.

    Args:
        interval (SiteCheckIntervalsCreate): The interval data to create.
        db (Session): The database session dependency.

    Returns:
        SiteCheckIntervalsBase: The created site check interval.

    Raises:
        HTTPException: If a database error occurs during commit.
    """
    db_interval = models.SiteCheckIntervals(
        site_url_id=interval.site_url_id,
        time_interval=interval.time_interval
    )
    db.add(db_interval)
    db.commit()
    db.refresh(db_interval)
    return db_interval


@router.get("/fetch", response_model=List[SiteCheckIntervalsBase])
async def fetch_intervals(db: db_dependency, interval_id: Optional[int] = Query(default=None)):
    """Fetch site check intervals.

    Args:
        db (Session): The database session dependency.
        interval_id (Optional[int], optional): ID of a specific interval to fetch.
            If not provided, all intervals are returned. Defaults to None.

    Returns:
        List[SiteCheckIntervalsBase]: A list of intervals if no interval_id is provided.
        SiteCheckIntervalsBase: A single interval if interval_id is provided.

    Raises:
        HTTPException: If an interval with the given ID is not found (404).
    """
    if interval_id is None:
        return db.query(models.SiteCheckIntervals).all()

    result = db.query(models.SiteCheckIntervals).filter(models.SiteCheckIntervals.id == interval_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Unable to find specified interval")
    
    return result


@router.patch("/update", response_model=SiteCheckIntervalsBase)
async def update_site_check_interval(
    interval_id: int, interval_update: SiteCheckIntervalsUpdate, db: db_dependency
):
    """Update a site check interval.

    Args:
        interval_id (int): ID of the interval to update.
        interval_update (SiteCheckIntervalsUpdate): Fields to update.
        db (Session): The database session dependency.

    Returns:
        SiteCheckIntervalsBase: The updated site check interval.

    Raises:
        HTTPException: If an interval with the given ID is not found (404).
    """
    interval = db.query(models.SiteCheckIntervals).filter(models.SiteCheckIntervals.id == interval_id).first()
    if not interval:
        raise HTTPException(status_code=404, detail="Unable to find specified interval")
    
    update_data = interval_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(interval, key, value)
    
    db.commit()
    db.refresh(interval)
    return interval


@router.delete("/delete")
async def delete_site_check_interval(interval_id: int, db: db_dependency):
    """Delete a site check interval by ID.

    Args:
        interval_id (int): ID of the interval to delete.
        db (Session): The database session dependency.

    Returns:
        str: Success message.

    Raises:
        HTTPException: If an interval with the given ID is not found (404).
    """
    interval = db.query(models.SiteCheckIntervals).filter(models.SiteCheckIntervals.id == interval_id).first()
    if not interval:
        raise HTTPException(status_code=404, detail="Unable to find specified interval")

    db.delete(interval)
    db.commit()

    return "Successfully deleted interval"
