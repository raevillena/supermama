
# Create service file
sudo nano /etc/systemd/system/web-automation.service


[Unit]
Description=Web Automation Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/home/$USER
ExecStart=/usr/bin/python3 /home/$USER/scheduler.py
Restart=always
RestartSec=10
Environment=DISPLAY=:0

[Install]
WantedBy=multi-user.target




# Replace $USER with your actual username
sudo sed -i "s/\$USER/$USER/g" /etc/systemd/system/web-automation.service

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable web-automation.service
sudo systemctl start web-automation.service

# Check status
sudo systemctl status web-automation.service

# View logs
journalctl -u web-automation.service -f