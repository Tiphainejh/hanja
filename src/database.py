# src/database.py
import sqlite3
from config import DATABASE_PATH

class DatabaseConnection:
    def __enter__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()