from scraper import scrape_new_jobs_only
from database import init_db, save_jobs, get_all_jobs, get_existing_ids
from telegram_bot import send_job_alert, send_message

def run():
    print("Starting job monitor...")
    init_db()
    
    # Get existing IDs from database
    existing_ids = get_existing_ids()
    print(f"Jobs already in database: {len(existing_ids)}")
    
    # Only scrape NEW jobs
    new_jobs = scrape_new_jobs_only(existing_ids)
    
    if new_jobs:
        save_jobs(new_jobs)
        send_message(f"🔍 Found {len(new_jobs)} new jobs!")
        for job in new_jobs:
            send_job_alert(job)
            print(f"Alert sent: {job['title']}")
    else:
        print("No new jobs found - no alerts sent")

if __name__ == "__main__":
    run()