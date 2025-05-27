from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
# Remove --headless to see what's happening
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://logger.mmsu.edu.ph/dtr/W3MjfXVR5mmjtuBX62byZAnBHpGCJu4YR9EWLrJvyfZuPpSXNq/3e4fbd92ff7fe35265113af58720926d")  # Replace with your URL
    
    # Find the element
    element = driver.find_element(By.ID, "id_number")
    
    print(f"Element found: {element}")
    print(f"Is displayed: {element.is_displayed()}")
    print(f"Height: {element.get_attribute('style')}")
    
    # Try to make it visible
    driver.execute_script("""
        var element = arguments[0];
        element.style.height = '40px';
        element.style.opacity = '1';
        element.style.visibility = 'visible';
    """, element)
    
    time.sleep(2)
    print(f"After JS - Is displayed: {element.is_displayed()}")
    
    # Try typing
    element.send_keys("TEST123")
    time.sleep(5)  # Wait to see the result
    
finally:
    driver.quit()