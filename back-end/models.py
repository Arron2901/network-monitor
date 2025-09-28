from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class MonitoredSites(Base):
    __tablename__ = "monitored_sites"

    id = Column(Integer, primary_key=True, index=True)
    site_url = Column(String, index=True)
    site_name = Column(String, index=True)

class SiteCheckIntervals(Base):
    __tablename__ = "site_check_intervals"

    id = Column(Integer, primary_key=True, index=True)
    site_url_id = Column(Integer, ForeignKey("monitored_sites.id"))
    time_interval = Column(Integer, default = 1)

class SiteStatus(Base):
    __tablename__ = "site_status"

    id = Column(Integer, primary_key=True, index=True)
    site_url_id = Column(Integer, ForeignKey("monitored_sites.id"))
    status = Column(Boolean, index=True)