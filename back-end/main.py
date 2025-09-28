# app/main.py
from fastapi import FastAPI, HTTPException, Depends
from Routers import monitored_sites_router  # import your router
import models
from database import engine, SessionLocal
from sqlalchemy.orm import session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# Include the router
app.include_router(monitored_sites_router.router)
