from celery import Celery
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import MonitoredSites, SiteStatus, Base
import requests
import os


celery_app = Celery(
    "celery_app",
    broker=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://redis:6379/0")
)


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:root@db:5432/networkmonitor")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@celery_app.task
def check_site(site_id: int):
    db = SessionLocal()
    try:
        site = db.query(MonitoredSites).filter(MonitoredSites.id == site_id).first()
        if not site:
            return

        interval_seconds = site.intervals[0].time_interval

        try:
            response = requests.get(site.site_url, timeout=5)
            status_value = response.status_code == 200
        except Exception:
            status_value = False

        site_status = site.statuses[0]
        site_status.status = status_value
        db.commit()

        print(f"[INFO] Checking site: {site.site_name} ({site.site_url})")
        print(f"[INFO] Status: {'UP' if status_value else 'DOWN'}")
        print(f"[INFO] Next check in {interval_seconds} seconds")

        check_site.apply_async((site.id,), countdown=interval_seconds)

    finally:
        db.close()


def schedule_all_sites():
    db = SessionLocal()
    try:
        sites = db.query(MonitoredSites).all()
        for site in sites:
            interval_seconds = site.intervals[0].time_interval
            
            check_site.apply_async((site.id,), countdown=interval_seconds)
    finally:
        db.close()


schedule_all_sites()
