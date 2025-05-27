#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'/home/{os.getenv("USER")}/automation.log'),
        logging.StreamHandler()
    ]
)

def setup_driver():
    """Configure Chrome with WebDriver Manager"""
    options = Options()
    
    # Run headless (no GUI)
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-extensions')
    
    try:
        # WebDriver Manager automatically downloads and manages ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        logging.error(f"Failed to initialize driver: {e}")
        return None

def web_automation_task():
    """Main automation function"""
    driver = None
    try:
        logging.info("Starting web automation task...")
        
        # Setup driver
        driver = setup_driver()
        if not driver:
            return False
            
        # Navigate to webpage - CHANGE THIS URL
        target_url = "https://www.google.com"  # Replace with your target URL
        logging.info(f"Opening {target_url}")
        driver.get(target_url)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Find input element - ADJUST THESE SELECTORS FOR YOUR TARGET SITE
        input_selectors = [
            "input[name='q']",  # Google search box
            "input[type='text']",
            "input[type='search']", 
            "#search",
            ".search-input",
            "textarea"
        ]
        
        input_element = None
        for selector in input_selectors:
            try:
                input_element = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                logging.info(f"Found input element with selector: {selector}")
                break
            except:
                continue
        
        if not input_element:
            logging.error("Could not find input element")
            return False
        
        # Input text - CHANGE THIS TEXT
        input_text = "Hello from automation script!"  # Replace with your text
        logging.info(f"Typing: {input_text}")
        
        input_element.clear()
        input_element.send_keys(input_text)
        
        # Press Enter
        logging.info("Pressing Enter")
        input_element.send_keys(Keys.RETURN)
        
        # Wait to see results
        time.sleep(3)
        
        # Optional: Take screenshot for verification
        screenshots_dir = f"/home/{os.getenv('USER')}/screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        screenshot_path = f"{screenshots_dir}/automation_{int(time.time())}.png"
        driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot saved: {screenshot_path}")
        
        logging.info("Task completed successfully")
        return True
        
    except Exception as e:
        logging.error(f"Automation failed: {e}")
        return False
        
    finally:
        if driver:
            driver.quit()
            logging.info("Browser closed")

if __name__ == "__main__":
    # Run the automation
    success = web_automation_task()
    exit(0 if success else 1)