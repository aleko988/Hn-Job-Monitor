import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_message(text):
    """Send a message to Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    return response.json()

def send_job_alert(job):
    """Format and send a job alert"""
    message = (
        f"🆕 <b>New Job Alert</b>\n\n"
        f"💼 <b>{job['title']}</b>\n"
        f"🏢 Company: {job['company']}\n"
        f"📅 Posted: {job['posted_at']}\n"
        f"🔗 <a href='{job['url']}'>Apply Here</a>"
    )
    return send_message(message)

if __name__ == "__main__":
    # Test message
    result = send_message("✅ Job Monitor is working correctly!")
    print(result)