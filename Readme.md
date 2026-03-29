# HN Job Monitor 🔍

Automated job monitoring system that scrapes HackerNews Jobs API every hour and sends instant Telegram alerts for new postings.

## What it does
- Scrapes HackerNews Jobs API automatically every hour
- Stores jobs in PostgreSQL database with duplicate detection
- Sends instant Telegram notifications for new jobs only
- REST API with public endpoints
- Deployed 24/7 on Railway

## Tech Stack
- Python
- FastAPI
- PostgreSQL
- Telegram Bot API
- Railway (deployment)
- cron-job.org (scheduling)

## Endpoints
| Endpoint | Description |
|----------|-------------|
| `/` | Health check |
| `/jobs` | Get all jobs as JSON |
| `/run` | Trigger scraper manually |
| `/dashboard` | View jobs in browser |

## Live Demo
- Dashboard: https://hn-job-monitor-production.up.railway.app/dashboard
- API: https://hn-job-monitor-production.up.railway.app/jobs

## Setup
1. Clone the repo
2. Create `.env` with `BOT_TOKEN`, `CHAT_ID`, `DATABASE_PUBLIC_URL`
3. Install requirements: `pip install -r requirements.txt`
4. Run locally: `python main_runner.py`
5. Deploy to Railway and add PostgreSQL

## How it works
```
cron-job.org (every hour)
        ↓
FastAPI /run endpoint
        ↓
Scraper fetches new job IDs from HN API
        ↓
New IDs saved to PostgreSQL
        ↓
Telegram alert sent for each new job
```