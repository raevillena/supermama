# Save the script
nano ~/web_automation.py
# Copy the script content and save

# Make executable
chmod +x ~/web_automation.py

# Edit crontab
crontab -e

# Schedule examples:
# Daily at 2:30 PM
30 14 * * * /usr/bin/python3 /home/$USER/web_automation.py

# Every 30 minutes
*/30 * * * * /usr/bin/python3 /home/$USER/web_automation.py

# Weekdays at 9 AM
0 9 * * 1-5 /usr/bin/python3 /home/$USER/web_automation.py
