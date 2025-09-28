# app/main.py
from fastapi import FastAPI
from Routers import monitored_urls_router, intervals_router, check_results_router  # import your router

app = FastAPI()

# Include the router
app.include_router(monitored_urls_router.router)
app.include_router(intervals_router.router)
app.include_router(check_results_router.router)