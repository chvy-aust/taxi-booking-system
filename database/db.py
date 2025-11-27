import sqlite3
from pathlib import Path
from typing import Any

DB_FILE = Path(__file__).parent.parent / 'taxibooking.db'

class DatabaseConnection:
    """Database class to handle transactions."""
    def __init__(self):
        self.db_path = DB_FILE
        self.connection: sqlite3.Connection | None = None

    def execute(self,
                sql: str,
                parameters: tuple | None = None
        ) -> sqlite3.Cursor:
        try:
            if parameters is not None:
                return self.connection.execute(sql, parameters)
            return self.connection.execute(sql)
        except sqlite3.Error as e:
            print(f"CRITICAL: {e}")
            raise

    def executemany(self,
                    sql: str,
                    parameters: tuple
        ) -> sqlite3.Cursor:
        try:
            return self.connection.executemany(sql, parameters)
        except sqlite3.Error as e:
            print(f"CRITICAL: {e}")
            raise

    def insert(self,
               table_name: str,
               record: dict[str, Any]
        ):
        values = tuple(record.values())
        fields = ','.join(record.keys())
        placeholders = ','.join("?" * len(record))
        self.execute(f"INSERT INTO {table_name} ({fields}) VALUES ({placeholders})", values)

    def fetch(self,
                  table_name: str,
                  conditions: str | tuple[str] | None = None,
                  params = None,
                  limit: int | None = None,
                  order_by: str | tuple[str] | None = None
                  ):
        sql = f"SELECT * FROM {table_name}"

        if conditions is not None:
            if isinstance(conditions, tuple):
                conditions = ' AND '.join(condition for condition in conditions)
            sql += f" WHERE {conditions}"

        if order_by is not None:
            if isinstance(conditions, tuple):
                order_by = ', '.join(_ for _ in order_by)
            sql += f" ORDER BY {order_by}"

        if limit is None:
            return self.execute(sql, params).fetchall()
        elif limit == 1:
            return self.execute(sql, params).fetchone()
        else:
            return self.execute(sql, params).fetchmany(limit)

    def get_user(self, email):
        return self.fetch(table_name="user", conditions="email = ?", params=(email,), limit=1)

    def __enter__(self):
        """Establish connection and return cursor."""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.row_factory = sqlite3.Row
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up transactions and close database."""
        if exc_type:
            self.connection.rollback()
        else:
            self.connection.commit()
        if self.connection:
            self.connection.close()

def create_user():
    return """
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        dob TEXT NOT NULL,
        phonenum TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        address TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """

def init_db():
    try:
        with DatabaseConnection() as conn:
            conn.execute(create_user())
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")

if __name__ == '__main__':
    init_db()