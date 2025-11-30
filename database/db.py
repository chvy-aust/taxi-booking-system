import sqlite3
from pathlib import Path
from typing import Any

DB_FILE = Path(__file__).parent.parent / 'taxibooking.db'

class DatabaseConnection:
    """Database class to handle transactions."""
    def __init__(self):
        self.db_path = DB_FILE
        self.conn: sqlite3.Connection | None = None

    def __enter__(self):
        """Establish connection and return cursor."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up transactions and close database."""
        if exc_type:
            self.conn.rollback()
            print(f"( WARNING ⚠ ) Transaction rolled back due to caught exception.\n"
                  f"( ⚠ ) {exc_type}: {exc_val}")
        else:
            self.conn.commit()

        if self.conn:
            self.conn.close()

    def execute(self, sql: str, params=()) -> sqlite3.Cursor:
        """Return easily accessible cursor.execute() method."""
        return self.conn.execute(sql, params)

    def lookup_user(self, email):
        cursor = self.execute("SELECT * FROM user WHERE email = ?", (email,))
        return cursor.fetchone()

    def create_user(self, firstname, lastname, dob, phonenum,
                    email, address, password, role="customer"):
        try:
            print(f"( ℹ ) Adding new user ({firstname} {lastname}) to database …")
            self.execute("""
                     INSERT INTO user (
                                role, firstname, lastname, dob,
                                phonenum, email, address, password)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                                """, (
                                role, firstname, lastname, dob,
                                phonenum, email, address, password,)
            )
        except sqlite3.Error as e:
            print(f"( WARNING ⚠ ) Failed to add user to database! ERROR: {e}")
            raise
        else:
            print(f"( ℹ ) Successfully added user to database!")

    def create_booking(self, customer_id: int, info: dict[str, Any]):

        # Append default data if booking is confirmed.
        driver_id = info.get("driver_id", None)
        status = info.get("status", "waiting_for_assignment")

        try:
            self.execute("""
                    INSERT INTO booking (
                                customer_id, driver_id, dropoff, 
                                pickup, date, time, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?) 
                                """, (
                                customer_id,
                                driver_id,
                                info["dropoff"],
                                info["pickup"],
                                info["date"],
                                info["time"],
                                status,)
            )
        except sqlite3.Error as e:
            print(f"( WARNING ⚠ ) Failed to make booking! ERROR: {e}")
            raise
        else:
            print(f"( ℹ ) Successfully created new booking!")