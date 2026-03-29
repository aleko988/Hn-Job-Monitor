from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    jobs = get_all_jobs()
    
    rows = ""
    for job in jobs:
        rows += f"""
        <tr>
            <td>{job[1]}</td>
            <td>{job[2]}</td>
            <td>{job[4]}</td>
            <td><a href="{job[3]}" target="_blank">Apply</a></td>
        </tr>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Job Monitor Dashboard</title>
        <style>
            body {{ font-family: Arial; margin: 20px; background: #f5f5f5; }}
            h1 {{ color: #2E75B6; }}
            table {{ width: 100%; border-collapse: collapse; background: white; }}
            th {{ background: #2E75B6; color: white; padding: 10px; text-align: left; }}
            td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
            tr:hover {{ background: #f0f0f0; }}
            a {{ color: #2E75B6; }}
        </style>
    </head>
    <body>
        <h1>HN Job Monitor</h1>
        <p>Total jobs: <strong>{len(jobs)}</strong></p>
        <table>
            <tr>
                <th>Title</th>
                <th>Company</th>
                <th>Posted</th>
                <th>Link</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """
    return html