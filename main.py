from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db, get_all_jobs
from main_runner import run

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"status": "Job Monitor is running"}

@app.get("/jobs")
def get_jobs():
    jobs = get_all_jobs()
    return {"total": len(jobs), "jobs": jobs}

@app.get("/run")
def run_scraper():
    run()
    return {"status": "Scraper executed successfully"}