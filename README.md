SolidDataEngineeringVPi 🌱
Solid Data Engineering for Raspberry Pi - Soil Monitoring System

A robust, production-ready soil monitoring system that collects sensor data and stores it in MySQL. Designed for reliable data engineering practices on Raspberry Pi hardware with enterprise-grade data pipeline architecture.

https://docs/system-architecture.png

🚀 Features
🌱 Multi-parameter Sensing - Moisture, temperature, pH, EC, nitrogen, phosphorus, potassium

💾 Enterprise Data Storage - MySQL integration with automatic sensor registration

📴 Offline Resilience - Local CSV storage with automatic sync when online

🤖 Production Deployment - Systemd service with auto-start and monitoring

🔧 Solid Data Pipeline - Error handling, retry logic, and comprehensive logging

📊 Real-time Monitoring - Continuous data collection with configurable intervals

🏗 System Architecture

🛠 Quick Installation
Prerequisites
Raspberry Pi 3 (or compatible)

NPK Soil Sensor with Modbus RTU

USB to RS485 Converter

MySQL Database Server

Automated Setup
bash
# Clone the repository
git clone https://github.com/yourusername/SolidDataEngineeringVPi.git
cd SolidDataEngineeringVPi

# Run the complete setup
chmod +x setup.sh
./setup.sh
The setup script will:

✅ Install all dependencies

✅ Configure serial port permissions

✅ Set up systemd service

✅ Enable auto-start on boot

✅ Start the service immediately

📁 Project Structure
text
SolidDataEngineeringVPi/
├── MainController.py          # Orchestrates the entire data pipeline
├── OnlineLogger.py            # MySQL database operations
├── OfflineLogger.py           # Local CSV storage management
├── SensorReader.py            # Modbus sensor communication
├── Config.py                  # Centralized configuration
├── setup.sh                   # Automated deployment script
├── requirements.txt           # Python dependencies
└── docs/
    ├── hardware-setup.md      # Wiring diagrams and connections
    ├── system-architecture.md # Data flow and components
    └── installation-guide.md  # Detailed setup instructions
⚙️ Configuration
Edit Config.py to customize your setup:

python
# Database Configuration
DB_CONFIG = {
    'user': "DevOps",
    'password': "DevTeam", 
    'host': "192.168.1.242",
    'port': 3306,
    'database': "soilmonitornig"
}

# Sensor Configuration
SERIAL_PORT = '/dev/ttyUSB0'    # Raspberry Pi serial port
MEASUREMENT_INTERVAL = 300      # 5-minute data collection intervals
🎯 Usage
Service Management
bash
# Check service status
sudo systemctl status soil-monitor.service

# View real-time logs
sudo journalctl -u soil-monitor.service -f

# Restart service
sudo systemctl restart soil-monitor.service

# Stop service
sudo systemctl stop soil-monitor.service
Sensor Assignment
Before data collection begins, assign your sensor to a farm:

sql
UPDATE sensors SET farm_id = 1 WHERE machine_id = 'YOUR_SENSOR_ID';
📊 Data Schema
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
🔧 Troubleshooting
Common Issues
Serial Port Not Found

bash
# Check connected devices
ls -la /dev/ttyUSB*

# Add user to dialout group
sudo usermod -a -G dialout $USER
Service Not Starting

bash
# Check service status
sudo systemctl status soil-monitor.service

# View detailed logs
sudo journalctl -u soil-monitor.service -n 50
Database Connection Issues

bash
# Test MySQL connection
mysql -h 192.168.1.242 -u DevOps -p -e "SHOW DATABASES;"
Log Analysis
bash
# Follow application logs in real-time
sudo journalctl -u soil-monitor.service -f

# Check for specific errors
sudo journalctl -u soil-monitor.service | grep -i error
🤝 Contributing
We welcome contributions! Please see our Contributing Guidelines for details.

Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🆘 Support
📖 Documentation

🐛 Issue Tracker

💬 Discussions

🙏 Acknowledgments
Raspberry Pi Foundation for the hardware platform

MySQL for robust data storage

Python ecosystem for comprehensive libraries

SolidDataEngineeringVPi - Building reliable data pipelines for agriculture, one sensor at a time. 🌱
