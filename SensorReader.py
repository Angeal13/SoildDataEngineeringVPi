import serial
import time
from datetime import datetime
import uuid
from Config import Config
import logging

class SensorReader:
    def __init__(self):
        self.serial_conn = self._init_serial()
        self.machine_id = str(uuid.getnode())  # Generate machine_id once
        logging.info(f"Sensor Machine ID: {self.machine_id}")
        
    def _init_serial(self):
        """Initialize serial connection with retries"""
        for attempt in range(3):
            try:
                ser = serial.Serial(
                    port=Config.SERIAL_PORT,
                    baudrate=Config.SERIAL_BAUDRATE,
                    timeout=Config.SERIAL_TIMEOUT
                )
                logging.info(f"Serial connected to {Config.SERIAL_PORT}")
                return ser
            except serial.SerialException as e:
                logging.warning(f"Serial attempt {attempt + 1} failed: {e}")
                if attempt == 2: return None
                time.sleep(2)

    def get_sensor_info(self):
        """Return sensor information for registration"""
        return {
            'machine_id': self.machine_id,
            'connection_timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def read_data(self):
        """Read and parse sensor data"""
        if not self.serial_conn:
            self.serial_conn = self._init_serial()
            if not self.serial_conn: return None

        try:
            # Send Modbus command
            self.serial_conn.write(Config.MODBUS_COMMAND)
            response = self.serial_conn.read(Config.RESPONSE_LENGTH)
            
            if not response:
                logging.warning("No sensor response")
                return None
                
            # Parse response (adapt to your protocol)
            return {
                'machine_id': self.machine_id,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'moisture': int.from_bytes(response[3:5], 'big') / 10,
                'temperature': int.from_bytes(response[5:7], 'big') / 10,
                'conductivity': int.from_bytes(response[7:9], 'big') / 10,
                'ph': int.from_bytes(response[9:11], 'big') / 10,
                'nitrogen': int.from_bytes(response[11:13], 'big') / 10,
                'phosphorus': int.from_bytes(response[13:15], 'big') / 10,
                'potassium': int.from_bytes(response[15:17], 'big') / 10
            }
        except Exception as e:
            logging.error(f"Sensor read failed: {e}")
            return None