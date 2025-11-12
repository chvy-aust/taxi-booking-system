import sqlite3
from pathlib import Path
from typing import Optional

DB_FILE = Path(__file__).parent / 'data.db'

class DatabaseConnection:
    """Database class to handle transactions."""
    def __init__(self):
        self.db_path = DB_FILE
        self.connection: Optional[sqlite3.Connection] = None

    def _check_transaction(self, *exception):
        """Rollback if exception caught in transaction, otherwise commit."""
        if exception:
            self.connection.rollback()
        else:
            self.connection.commit()

    def __enter__(self):
        """Establish connection and return cursor."""
        self.connection = sqlite3.connect(self.db_path)
        # Return data as dictionaries.
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        # Return cursor to execute queries.
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up transactions and close database."""
        self._check_transaction()
        self.connection.close()



def main():
    try:
        with DatabaseConnection() as connection:
            # Execute table creation statements here.
            print("Successfully initialized database.")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")

if __name__ == '__main__':
    main()