#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    """Configure Chrome for Ubuntu 20.04"""
    options = Options()
    
    # Run headless (no GUI)
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    # Additional stability options
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--disable-extensions')
    
    try:
        # ChromeDriver should be in PATH after installation
        driver = webdriver.Chrome(options=options)
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
            
        # Navigate to webpage
        target_url = "https://example.com"  # Replace with your URL
        logging.info(f"Opening {target_url}")
        driver.get(target_url)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Find input element (adjust selector as needed)
        input_selectors = [
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
                break
            except:
                continue
        
        if not input_element:
            logging.error("Could not find input element")
            return False
        
        # Clear any existing text and input new text
        input_text = "Your automated input here"  # Replace with your text
        logging.info(f"Typing: {input_text}")
        
        input_element.clear()
        input_element.send_keys(input_text)
        
        # Press Enter
        logging.info("Pressing Enter")
        input_element.send_keys(Keys.RETURN)
        
        # Optional: Wait to see results
        time.sleep(2)
        
        # Optional: Take screenshot for verification
        screenshot_path = f"/home/{os.getenv('USER')}/screenshots/automation_{int(time.time())}.png"
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
    # Create screenshots directory
    import os
    screenshots_dir = f"/home/{os.getenv('USER')}/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    # Run the automation
    success = web_automation_task()
    exit(0 if success else 1)