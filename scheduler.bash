#!/usr/bin/env python3

import schedule
import time
import logging
from web_automation import web_automation_task  # Import your main function

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'/home/{os.getenv("USER")}/scheduler.log'),
        logging.StreamHandler()
    ]
)

def scheduled_job():
    """Wrapper for the automation task"""
    logging.info("=== Starting scheduled automation ===")
    try:
        success = web_automation_task()
        if success:
            logging.info("=== Automation completed successfully ===")
        else:
            logging.error("=== Automation failed ===")
    except Exception as e:
        logging.error(f"=== Scheduler error: {e} ===")

# Schedule options - uncomment the one you want
schedule.every().day.at("14:30").do(scheduled_job)  # Daily at 2:30 PM
# schedule.every(30).minutes.do(scheduled_job)  # Every 30 minutes
# schedule.every().monday.at("09:00").do(scheduled_job)  # Monday at 9 AM
# schedule.every().hour.do(scheduled_job)  # Every hour

if __name__ == "__main__":
    logging.info("Scheduler started. Waiting for scheduled times...")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user")
    except Exception as e:
        logging.error(f"Scheduler crashed: {e}")