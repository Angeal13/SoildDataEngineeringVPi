import mysql.connector
from Config import Config
import logging
import time

class OnlineLogger:
    def __init__(self):
        self.conn = self._init_db()
        
    def _init_db(self):
        """Initialize database connection with retries"""
        for attempt in range(3):
            try:
                conn = mysql.connector.connect(**Config.DB_CONFIG)
                logging.info("Connected to MySQL database")
                return conn
            except mysql.connector.Error as e:
                logging.warning(f"DB attempt {attempt + 1} failed: {e}")
                if attempt == 2: return None
                time.sleep(5)

    def register_sensor(self, sensor_info):
        """Register a new sensor in the SENSORS table WITHOUT installation date"""
        if not self.conn:
            self.conn = self._init_db()
            if not self.conn: 
                logging.error("Failed to establish database connection")
                return False

        try:
            cur = self.conn.cursor()
            
            # Check if sensor already exists
            cur.execute("SELECT COUNT(*) FROM sensors WHERE machine_id = %s", 
                    (sensor_info['machine_id'],))
            
            if cur.fetchone()[0] == 0:
                # Register new sensor with NULL installation date (will be set during assignment)
                insert_query = """
                INSERT INTO sensors (machine_id, installation)
                VALUES (%s, NULL)
                """
                cur.execute(insert_query, (sensor_info['machine_id'],))
                self.conn.commit()
                logging.info(f"New sensor registered: {sensor_info['machine_id']}")
                return True
            else:
                logging.info(f"Sensor already registered: {sensor_info['machine_id']}")
                return True
                
        except mysql.connector.Error as e:
            logging.error(f"Sensor registration failed: {e}")
            if self.conn:
                self.conn.rollback()
            return False

    def save(self, data):
        """Save data to MySQL - assumes sensor is already registered"""
        if not self.conn:
            self.conn = self._init_db()
            if not self.conn: 
                logging.error("Failed to establish database connection")
                return False

        try:
            cur = self.conn.cursor()
            query = '''INSERT INTO soildata
                    (machine_id, timestamp, moisture, temperature, ec, ph, n, p, k)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            
            logging.info(f"Inserting data: {data}")
            
            cur.execute(query, (
                data['machine_id'],
                data['timestamp'],
                data['moisture'],
                data['temperature'],
                data['conductivity'],  # This maps to 'ec' in database
                data['ph'],
                data['nitrogen'],
                data['phosphorus'],
                data['potassium']
            ))
            self.conn.commit()
            logging.info("Data successfully saved to database")
            return True
        except mysql.connector.Error as e:
            logging.error(f"Database save failed: {e}")
            if self.conn:
                self.conn.rollback()
            
            # If it's a foreign key error, try to register the sensor
            if "foreign key constraint" in str(e).lower():
                logging.info("Attempting to register sensor due to foreign key error")
                sensor_info = {
                    'machine_id': data['machine_id']
                }
                if self.register_sensor(sensor_info):
                    # Retry the save operation
                    return self.save(data)
            
            return False
        except Exception as e:
            logging.error(f"Unexpected error in save: {e}")
            return False