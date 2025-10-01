# app/main.py
from fastapi import FastAPI, HTTPException, Depends
from Routers import monitored_sites_router, check_site_intervals_router, site_status_router  # import your router
import models
from database import engine, SessionLocal
from sqlalchemy.orm import session
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your Next.js URL
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include the router
app.include_router(monitored_sites_router.router)
app.include_router(check_site_intervals_router.router)
app.include_router(site_status_router.router)
