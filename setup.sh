#!/bin/bash

echo "=================================================="
echo "Soil Monitoring System Setup for Raspberry Pi 3"
echo "=================================================="

# Check if running on Raspberry Pi
if ! command -v raspi-config &> /dev/null; then
    echo "Warning: This script is designed for Raspberry Pi systems."
    echo "Continue anyway? (y/N): "
    read answer
    if [ "$answer" != "${answer#[Yy]}" ] ; then
        echo "Continuing setup..."
    else
        echo "Setup cancelled."
        exit 1
    fi
fi

# Update system
echo ""
echo "Step 1: Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install required system packages
echo ""
echo "Step 2: Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv git

# Add user to dialout group for serial port access
echo ""
echo "Step 3: Setting up serial port permissions..."
sudo usermod -a -G dialout $USER

# Install Python packages
echo ""
echo "Step 4: Installing Python packages..."
pip3 install mysql-connector-python
pip3 install pyserial
pip3 install pandas

# Create application directory
echo ""
echo "Step 5: Setting up application directory..."
sudo mkdir -p /opt/SoildDataEngineeringVPi
sudo chown -R $USER:$USER /opt/SoildDataEngineeringVPi

# Copy application files
echo ""
echo "Step 6: Copying application files..."
# Check if files exist in current directory
if [ -f "MainController.py" ]; then
    cp *.py /opt/SoildDataEngineeringVPi/
    echo "Application files copied successfully."
else
    echo "Error: Application files not found in current directory."
    echo "Please ensure all Python files are in the same directory as setup.sh"
    exit 1
fi

# Create data directory for offline storage
mkdir -p /opt/SoildDataEngineeringVPi/data
chmod 755 /opt/SoildDataEngineeringVPi/data

# Create systemd service file
echo ""
echo "Step 7: Creating system service..."
sudo tee /etc/systemd/system/soil-monitor.service > /dev/null <<EOF
[Unit]
Description=Soil Monitoring System
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/soil_monitor
ExecStart=/usr/bin/python3 /opt/soil_monitor/MainController.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
echo ""
echo "Step 8: Configuring service..."
sudo systemctl daemon-reload
sudo systemctl enable soil-monitor.service

# Set permissions
sudo chmod 644 /etc/systemd/system/soil-monitor.service

# Start the service immediately
echo ""
echo "Step 9: Starting soil monitor service..."
sudo systemctl start soil-monitor.service

# Wait a moment for service to initialize
sleep 5

# Verify service status
echo ""
echo "Step 10: Verifying service status..."
SERVICE_STATUS=$(sudo systemctl is-active soil-monitor.service)

if [ "$SERVICE_STATUS" = "active" ]; then
    echo "✅ Service is running successfully!"
else
    echo "⚠️  Service started but may not be fully active yet"
    echo "Service status: $SERVICE_STATUS"
fi

echo ""
echo "=================================================="
echo "Setup Completed Successfully!"
echo "=================================================="
echo ""
echo "What was installed:"
echo "✅ System dependencies (Python, git)"
echo "✅ Python packages (mysql-connector, pyserial, pandas)"
echo "✅ Application files in /opt/soil_monitor/"
echo "✅ System service (auto-start on boot)"
echo "✅ Serial port permissions"
echo ""
echo "*** IMPORTANT: REBOOT REQUIRED ***"
echo "A reboot is required to apply serial port permissions."
echo ""
echo "Next steps after reboot:"
echo "1. Assign your sensor to a farm in the database:"
echo "   UPDATE sensors SET farm_id = 1 WHERE machine_id = 'YOUR_SENSOR_ID';"
echo "2. Check service status: sudo systemctl status soil-monitor.service"
echo "3. View logs: journalctl -u soil-monitor.service -f"
echo ""
echo -n "Do you want to reboot now? (recommended) (y/N): "
read answer

if [ "$answer" != "${answer#[Yy]}" ] ; then
    echo ""
    echo "Rebooting system in 5 seconds..."
    echo "The soil monitor service will start automatically after reboot."
    sleep 5
    sudo reboot
else
    echo ""
    echo "Please reboot manually when convenient:"
    echo "  sudo reboot"
    echo ""
    echo "The service will not be able to access serial ports until reboot."
fi

echo ""
echo "Management commands for future reference:"
echo "  Check status: sudo systemctl status soil-monitor.service"
echo "  Stop service: sudo systemctl stop soil-monitor.service"
echo "  Start service: sudo systemctl start soil-monitor.service"
echo "  Restart service: sudo systemctl restart soil-monitor.service"
echo "  View logs: journalctl -u soil-monitor.service -f"
