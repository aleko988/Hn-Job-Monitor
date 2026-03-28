import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            company TEXT,
            url TEXT UNIQUE NOT NULL,
            posted_at TEXT,
            scraped_at TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialized")

def save_jobs(jobs):
    """
    Save jobs to database.
    Returns only NEW jobs that weren't in database before.
    """
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    
    new_jobs = []
    for job in jobs:
        try:
            cursor.execute("""
                INSERT INTO jobs (id, title, company, url, posted_at, scraped_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                job["id"],
                job["title"],
                job["company"],
                job["url"],
                job["posted_at"],
                job["scraped_at"]
            ))
            new_jobs.append(job)
        except sqlite3.IntegrityError:
            # Already exists - skip
            pass
    
    conn.commit()
    conn.close()
    return new_jobs

def get_all_jobs():
    """Return all jobs from database"""
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs ORDER BY posted_at DESC")
    jobs = cursor.fetchall()
    conn.close()
    return jobs

if __name__ == "__main__":
    init_db()
    print(f"Total jobs in database: {len(get_all_jobs())}")