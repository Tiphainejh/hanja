#! @file src/database.py
import sqlite3
from src.config import DATABASE_PATH

class DatabaseConnection:
    """!
    @brief A class to manage database connections using a context manager.
    Provides a convenient way to handle SQLite connections, ensuring
    the connection is properly closed after use.
    """

    def __enter__(self):
        """!
        @brief Establishes a connection to the SQLite database.

        @return sqlite3.Connection object representing the database connection.
        """
        self.conn = sqlite3.connect(DATABASE_PATH)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """!
        @brief Closes the database connection when exiting the context.

        @param exc_val The value of the exception (if any).
        @param exc_type The type of the exception (if any).
        @param exc_tb The traceback of the exception (if any).
        """
        if self.conn:
            self.conn.close()
