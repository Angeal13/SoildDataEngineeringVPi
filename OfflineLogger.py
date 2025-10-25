import pandas as pd
from Config import Config
import os
import logging

class OfflineLogger:
    def __init__(self):
        self.storage_path = Config.OFFLINE_STORAGE
        
    def save(self, data):
        """Append data to CSV with size limits"""
        try:
            df = pd.DataFrame([data])
            if os.path.exists(self.storage_path):
                existing = pd.read_csv(self.storage_path)
                df = pd.concat([existing, df]).tail(Config.MAX_OFFLINE_RECORDS)
            df.to_csv(self.storage_path, index=False)
            logging.info(f"Stored offline (Total: {len(df)})")
            return True
        except Exception as e:
            logging.error(f"Offline save failed: {e}")
            return False

    def load_all(self):
        """Load all offline records"""
        if os.path.exists(self.storage_path):
            return pd.read_csv(self.storage_path)
        return pd.DataFrame()

    def clear(self):
        """Delete offline storage"""
        try:
            os.remove(self.storage_path)
            return True
        except Exception as e:
            logging.error(f"Failed to clear offline data: {e}")
            return False