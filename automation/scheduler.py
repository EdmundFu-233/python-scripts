"""Simple task scheduler"""
import time
import schedule
from datetime import datetime

def job(name: str):
    print(f"[{datetime.now().isoformat()}] Running: {name}")

def backup_job():
    job("Daily backup")

def cleanup_job():
    job("Weekly cleanup")

def report_job():
    job("Hourly report")

def main():
    schedule.every().day.at("02:00").do(backup_job)
    schedule.every().monday.at("03:00").do(cleanup_job)
    schedule.every().hour.do(report_job)
    
    print("Scheduler started. Press Ctrl+C to stop.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("Scheduler stopped")

if __name__ == "__main__":
    main()
