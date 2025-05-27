#!/usr/bin/env python3

import schedule
import time
import logging
import os
import subprocess
import random
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'/home/{os.getenv("USER")}/scheduler.log'),
        logging.StreamHandler()
    ]
)

def run_automation():
    """Run the web automation script"""
    logging.info("=== Starting scheduled automation ===")
    try:
        # Run the automation script
        result = subprocess.run(
            ['/usr/bin/python3', f'/home/{os.getenv("USER")}/supermama/main.py'],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            logging.info("=== Automation completed successfully ===")
        else:
            logging.error(f"=== Automation failed with code {result.returncode} ===")
            logging.error(f"Error output: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        logging.error("=== Automation timed out ===")
    except Exception as e:
        logging.error(f"=== Scheduler error: {e} ===")

def schedule_random_weekday_times():
    """Schedule random times between 7:30-7:55 AM for Monday-Friday"""
    
    # Clear existing jobs
    schedule.clear()
    
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    
    for day in weekdays:
        # Generate random time between 7:30 and 7:55
        random_minute = random.randint(30, 55)
        time_str = f"07:{random_minute:02d}"
        
        # Schedule for this weekday
        getattr(schedule.every(), day).at(time_str).do(run_automation)
        logging.info(f"Scheduled for {day.capitalize()} at {time_str}")

def reschedule_weekly():
    """Reschedule with new random times every week"""
    logging.info("=== Rescheduling with new random times ===")
    schedule_random_weekday_times()
    
    # Show next scheduled times
    logging.info("New schedule:")
    for job in schedule.jobs:
        logging.info(f"  {job}")

if __name__ == "__main__":
    # Initial scheduling
    schedule_random_weekday_times()
    
    # Schedule weekly rescheduling (every Sunday at midnight)
    schedule.every().sunday.at("00:01").do(reschedule_weekly)
    
    logging.info("Random scheduler started. Current schedule:")
    for job in schedule.jobs:
        logging.info(f"  {job}")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user")
    except Exception as e:
        logging.error(f"Scheduler crashed: {e}")