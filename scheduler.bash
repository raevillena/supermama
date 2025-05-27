#!/usr/bin/env python3

import schedule
import time
import logging
import os
import subprocess

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
            ['/usr/bin/python3', f'/home/{os.getenv("USER")}/web_automation.py'],
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

# Schedule the automation - MODIFY THESE AS NEEDED
schedule.every().day.at("14:30").do(run_automation)  # Daily at 2:30 PM
# schedule.every(30).minutes.do(run_automation)      # Every 30 minutes
# schedule.every().monday.at("09:00").do(run_automation)  # Monday at 9 AM

if __name__ == "__main__":
    logging.info("Scheduler started. Next run times:")
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