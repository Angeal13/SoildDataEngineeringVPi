can i have the readme file?
Soil Monitoring System for Raspberry Pi
Overview
A Python-based soil monitoring system that collects sensor data and stores it in a MySQL database. Designed to run on Raspberry Pi 3 with automatic startup. The system reads soil parameters including moisture, temperature, pH, conductivity, and NPK levels via Modbus protocol.

Features
🌱 Multi-parameter sensing: Moisture, temperature, pH, EC, nitrogen, phosphorus, potassium

💾 MySQL integration: Secure data storage with automatic sensor registration

📴 Offline capability: Local CSV storage when internet is unavailable

🔄 Auto-sync: Automatically syncs offline data when connection is restored

🤖 Auto-start service: Runs automatically on boot via systemd

🔧 Easy setup: One-command installation and configuration

Hardware Requirements
Raspberry Pi 3 (or compatible)

Soil sensor with Modbus RTU interface

USB to RS485 converter (if sensor uses RS485)

Internet connection for database communication

Quick Installation
Clone the repository:

bash
git clone <your-repo-url>
cd soil-monitor
Run the setup script:

bash
chmod +x setup.sh
./setup.sh
Follow the prompts to reboot your Raspberry Pi

Assign your sensor to a farm in the database:

sql
UPDATE sensors SET farm_id = 1 WHERE machine_id = 'YOUR_SENSOR_ID';
Service Management
The system runs as a service that starts automatically on boot.

Check Status
bash
sudo systemctl status soil-monitor.service
View Logs
bash
# Follow logs in real-time
journalctl -u soil-monitor.service -f

# View recent logs
journalctl -u soil-monitor.service --since "1 hour ago"
Manual Control
bash
# Stop the service
sudo systemctl stop soil-monitor.service

# Start the service
sudo systemctl start soil-monitor.service

# Restart the service
sudo systemctl restart soil-monitor.service
Configuration
Edit Config.py to customize settings:

Database Connection
python
DB_CONFIG = {
    'user': "your_username",
    'password': "your_password", 
    'host': "your_database_host",
    'port': 3306,
    'database': "soilmonitornig"
}
Sensor Settings
python
SERIAL_PORT = '/dev/ttyUSB0'  # Change if using different port
MEASUREMENT_INTERVAL = 300    # Seconds between readings (5 minutes)
Database Schema
Ensure your MySQL database has these tables:

Sensors Table
sql
CREATE TABLE sensors (
    machine_id VARCHAR(255) PRIMARY KEY,
    farm_id INT NULL,
    installation TIMESTAMP NULL
);
Soil Data Table
sql
CREATE TABLE soildata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    machine_id VARCHAR(255),
    timestamp DATETIME,
    moisture DECIMAL(5,2),
    temperature DECIMAL(5,2),
    ec DECIMAL(5,2),
    ph DECIMAL(5,2),
    n DECIMAL(5,2),
    p DECIMAL(5,2),
    k DECIMAL(5,2),
    FOREIGN KEY (machine_id) REFERENCES sensors(machine_id)
);
Troubleshooting
Serial Port Issues
bash
# Check available serial devices
ls -la /dev/tty*

# Verify user is in dialout group
groups $USER
Service Won't Start
Check service status: sudo systemctl status soil-monitor.service

View detailed logs: journalctl -u soil-monitor.service

Verify database connectivity and sensor assignment

No Data Collection
Ensure sensor is assigned to a farm in the database

Check serial connection to sensor

Verify Modbus communication parameters

File Structure
text
/opt/soil_monitor/
├── MainController.py      # Main application controller
├── OnlineLogger.py        # MySQL database operations
├── OfflineLogger.py       # Local CSV storage
├── SensorReader.py        # Modbus sensor communication
├── Config.py             # Configuration settings
└── data/
    └── offline_data.csv  # Offline data storage
Dependencies
Python 3

mysql-connector-python

pyserial

pandas

All dependencies are automatically installed by the setup script.

Support
For issues and questions:

Check the troubleshooting section above

Review service logs with journalctl -u soil-monitor.service

Ensure all hardware connections are secure
