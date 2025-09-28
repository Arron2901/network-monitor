from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class MonitoredURL(Base):
    __tablename__ = "monitored_urls"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True,index=True)
    url = Column(String, unique=True, index=True)
    is_up = Column(Boolean, default=True)
    last_checked = Column(DateTime(timezone=True), server_default=func.now())

class CheckResult(Base):
    __tablename__ = "check_results"

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer)
    response_time = Column(Integer)

class Intervals(Base):
    __tablename__ = "intervals"

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer)
    time_interval = Column(Integer)