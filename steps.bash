1. Install Required Packages
    # Update system
    sudo apt update

    # Install Python and pip
    sudo apt install python3 python3-pip -y

    # Install Google Chrome
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
    sudo apt update
    sudo apt install google-chrome-stable -y

    # Install Python packages
    pip3 install selenium webdriver-manager schedule

2. Create the Main Automation Script

3. Save and Test the Script
    # Save the script
    nano ~/web_automation.py
    # Copy the script content above and save (Ctrl+X, Y, Enter)

    # Make it executable
    chmod +x ~/web_automation.py

    # Test the script
    python3 ~/web_automation.py

4. Create Scheduler Script (Optional)
    # Save scheduler script
    nano ~/scheduler.py
    # Copy the scheduler content and save

    # Make executable
    chmod +x ~/scheduler.py

5. Testing Steps
    python3 -c "
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    print('Testing Chrome and WebDriver Manager...')
    options = Options()
    options.add_argument('--headless')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://www.google.com')
    print(f'Success! Page title: {driver.title}')
    driver.quit()
    print('Test completed successfully!')
    "

    Test 2: Run Your Automation Script
        # Run the main script
        python3 ~/web_automation.py

        # Check the log
        cat ~/automation.log

        # Check if screenshot was created
        ls -la ~/screenshots/

    Test 3: Test Scheduler (Optional)
        # Run scheduler for a few minutes to test
        timeout 120 python3 ~/scheduler.py

        # Check scheduler log
        cat ~/scheduler.log


6. Set Up Cron for Scheduling
    # Edit crontab
    crontab -e

    # Add one of these lines (uncomment the one you want):
    # Daily at 2:30 PM
    30 14 * * * /usr/bin/python3 /home/$USER/web_automation.py >> /home/$USER/cron.log 2>&1

    # Every 30 minutes
    # */30 * * * * /usr/bin/python3 /home/$USER/web_automation.py >> /home/$USER/cron.log 2>&1

    # Weekdays at 9 AM
    # 0 9 * * 1-5 /usr/bin/python3 /home/$USER/web_automation.py >> /home/$USER/cron.log 2>&1

7. Monitor and Debug
    # Watch automation log in real-time
    tail -f ~/automation.log

    # Check cron log
    tail -f ~/cron.log

    # View all screenshots
    ls -la ~/screenshots/

    # Test cron job manually
    /usr/bin/python3 /home/$USER/web_automation.py

8. Customize for Your Use Case
    Edit ~/web_automation.py and change:

    target_url: Your target website
    input_text: The text you want to type
    input_selectors: CSS selectors for your target site's input fields


