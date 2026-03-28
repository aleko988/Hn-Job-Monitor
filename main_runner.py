from scraper import scrape_hn_jobs
from database import init_db, save_jobs, get_all_jobs
from telegram_bot import send_job_alert, send_message

def run():
    print("Starting job monitor...")
    
    # Initialize database
    init_db()
    
    # Scrape jobs
    jobs = scrape_hn_jobs(limit=50)
    
    # Save to database - returns only NEW jobs
    new_jobs = save_jobs(jobs)
    
    print(f"\nTotal scraped: {len(jobs)}")
    print(f"New jobs found: {len(new_jobs)}")
    print(f"Total in database: {len(get_all_jobs())}")
    
    if new_jobs:
        send_message(f"🔍 Found {len(new_jobs)} new jobs!")
        for job in new_jobs:
            send_job_alert(job)
            print(f"Alert sent: {job['title']}")
    else:
        print("No new jobs found - no alerts sent")

if __name__ == "__main__":
    run()