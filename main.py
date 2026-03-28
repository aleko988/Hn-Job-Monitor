from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db, get_all_jobs
from main_runner import run
import schedule
import time
import threading

def run_scheduler():
    schedule.every(1).hours.do(run)
    while True:
        schedule.run_pending()
        time.sleep(60)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    # Run scraper once on startup
    run()
    # Start scheduler in background thread
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()
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