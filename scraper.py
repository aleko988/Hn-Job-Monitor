import requests
from datetime import datetime
import time

BASE_URL = "https://hacker-news.firebaseio.com/v0"

def get_job_ids():
    """Fetch all available job IDs from HackerNews"""
    response = requests.get(f"{BASE_URL}/jobstories.json", timeout=10)
    response.raise_for_status()
    return response.json()

def get_job_details(job_id):
    """Fetch details for a single job by ID"""
    response = requests.get(f"{BASE_URL}/item/{job_id}.json", timeout=10)
    response.raise_for_status()
    return response.json()

def scrape_hn_jobs(limit=50):
    """
    Main scraper function
    limit: how many jobs to fetch (None = fetch all)
    """
    print("Fetching job IDs...")
    job_ids = get_job_ids()
    print(f"Total jobs available: {len(job_ids)}")
    
    if limit:
        job_ids = job_ids[:limit]
        print(f"Fetching first {limit} jobs...")
    
    jobs = []
    failed = 0
    
    for index, job_id in enumerate(job_ids, 1):
        try:
            job_data = get_job_details(job_id)
            
            if not job_data:
                failed += 1
                continue
                
            jobs.append({
                "id": job_id,
                "title": job_data.get("title", "No title"),
                "company": extract_company(job_data.get("title", "")),
                "url": job_data.get("url", f"https://news.ycombinator.com/item?id={job_id}"),
                "posted_at": datetime.fromtimestamp(
                    job_data.get("time", 0)
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "scraped_at": str(datetime.now())
            })
            
            print(f"[{index}/{len(job_ids)}] {job_data.get('title', 'No title')}")
            
            # Be respectful to the API - small delay
            time.sleep(0.1)
            
        except requests.RequestException as e:
            print(f"Failed to fetch job {job_id}: {e}")
            failed += 1
            continue
    
    print(f"\nDone. Fetched: {len(jobs)} | Failed: {failed}")
    return jobs

def extract_company(title):
    """
    Extract company name from HN job title
    Most titles follow pattern: 'Company (YC XX) is hiring...'
    """
    if "(" in title:
        return title.split("(")[0].strip()
    if " is hiring" in title.lower():
        return title.lower().split(" is hiring")[0].strip().title()
    return "Unknown"
def get_new_job_ids(existing_ids):
    """Only return IDs that aren't in database yet"""
    all_ids = get_job_ids()
    new_ids = [id for id in all_ids if id not in existing_ids]
    return new_ids

def scrape_new_jobs_only(existing_ids):
    """Only fetch details for new jobs"""
    new_ids = get_new_job_ids(existing_ids)
    
    if not new_ids:
        print("No new job IDs found")
        return []
    
    print(f"Found {len(new_ids)} new job IDs - fetching details...")
    jobs = []
    for job_id in new_ids:
        try:
            job_data = get_job_details(job_id)
            if job_data:
                jobs.append({
                    "id": job_id,
                    "title": job_data.get("title", "No title"),
                    "company": extract_company(job_data.get("title", "")),
                    "url": job_data.get("url", f"https://news.ycombinator.com/item?id={job_id}"),
                    "posted_at": datetime.fromtimestamp(
                        job_data.get("time", 0)
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                    "scraped_at": str(datetime.now())
                })
            time.sleep(0.1)
        except Exception as e:
            print(f"Failed to fetch job {job_id}: {e}")
            continue
    
    return jobs

if __name__ == "__main__":
    jobs = scrape_hn_jobs(limit=50)
    print(f"\nSample output:")
    for job in jobs[:3]:
        print(job)