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
        target_url = "https://logger.mmsu.edu.ph/dtr/W3MjfXVR5mmjtuBX62byZAnBHpGCJu4YR9EWLrJvyfZuPpSXNq/3e4fbd92ff7fe35265113af58720926d"  # Replace with your target URL
        logging.info(f"Opening {target_url}")
        driver.get(target_url)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Find input element - Handle initially hidden ID input
        input_selectors = [
            "#id_number",                    # ID selector (most reliable)
            "input[name='id_number']",       # Name attribute selector
            "input[id='id_number']",         # ID attribute selector
        ]
        
        input_element = None
        for selector in input_selectors:
            try:
                # First, try to find the element (even if hidden)
                input_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                logging.info(f"Found input element with selector: {selector}")
                
                # Check if element is visible
                if input_element.is_displayed():
                    logging.info("Element is visible")
                else:
                    logging.info("Element found but hidden - attempting to make visible")
                    
                    # Try clicking somewhere on the page to activate the field
                    body = driver.find_element(By.TAG_NAME, "body")
                    body.click()
                    time.sleep(1)
                    
                    # Or try executing JavaScript to make it visible
                    driver.execute_script("""
                        var element = arguments[0];
                        element.style.height = '40px';
                        element.style.opacity = '1';
                        element.style.visibility = 'visible';
                    """, input_element)
                    
                    time.sleep(1)
                
                # Try to make it clickable
                input_element = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                break
                
            except Exception as e:
                logging.warning(f"Selector {selector} failed: {e}")
                continue
        
        if not input_element:
            logging.error("Could not find input element")
            return False
        
        # Input text - Your ID number
        input_text = "0855629315"  # Replace with your actual ID number
        logging.info(f"Typing: {input_text}")
        
        # Clear and type - handle hidden element
        try:
            # Focus on the element first
            driver.execute_script("arguments[0].focus();", input_element)
            
            # Clear and type
            input_element.clear()
            input_element.send_keys(input_text)
            
        except Exception as e:
            logging.warning(f"Normal input failed, trying JavaScript: {e}")
            # If normal typing fails, use JavaScript
            driver.execute_script("""
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, input_element, input_text)
        
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