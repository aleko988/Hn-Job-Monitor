import schedule
import time
from main_runner import run
from telegram_bot import send_message

def scheduled_run():
    print("\n⏰ Scheduled check starting...")
    run()

if __name__ == "__main__":
    print("🚀 Job Monitor Scheduler Started")
    print("Checking for new jobs every 1 hour")
    send_message("🚀 Job Monitor started - checking every 1 hour")
    
    # Run immediately on start
    scheduled_run()
    
    # Then run every 1 hour
    schedule.every(1).hours.do(scheduled_run)
    
    while True:
        schedule.run_pending()
        time.sleep(60)