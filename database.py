import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id BIGINT PRIMARY KEY,
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
    conn = get_conn()
    cursor = conn.cursor()
    
    new_jobs = []
    for job in jobs:
        try:
            cursor.execute("""
                INSERT INTO jobs (id, title, company, url, posted_at, scraped_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                job["id"],
                job["title"],
                job["company"],
                job["url"],
                job["posted_at"],
                job["scraped_at"]
            ))
            if cursor.rowcount > 0:
                new_jobs.append(job)
        except Exception as e:
            print(f"Error saving job {job['id']}: {e}")
            continue
    
    conn.commit()
    conn.close()
    return new_jobs

def get_all_jobs():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs ORDER BY posted_at DESC")
    jobs = cursor.fetchall()
    conn.close()
    return jobs

if __name__ == "__main__":
    init_db()
    print(f"Total jobs in database: {len(get_all_jobs())}")