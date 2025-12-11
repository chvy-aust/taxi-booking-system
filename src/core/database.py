import logging
import sqlite3
from typing import Any

from src.core.models import User, Booking
from src.utils.constants import DB_FILE

logger = logging.getLogger(__name__)
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
        else:
            self.conn.commit()

        if self.conn:
            self.conn.close()

    def execute(self, sql: str, params=()) -> sqlite3.Cursor:
        """Return easily accessible cursor.execute() method."""
        try:
            cursor = self.conn.execute(sql, params)
            return cursor
        except sqlite3.Error as e:
            logger.exception(e)
            raise

    def lookup_user(self, email):
        """Return a User instance or None if no user is fetched."""
        cursor = self.execute(
            "SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if not row:
            return None
        return User(row)

    def fetch_bookings(self,
                       user_id: int = None,
                       user_role: str = "customer"):
        """
        Return a list of queried Booking instances.
        Accepts an optional user id condition.
        """
        sql = "SELECT * FROM bookings"
        params = None

        if user_id:
            sql += f" WHERE {user_role}_id = ?"
            params = (user_id,)

        cursor = self.execute(sql, params)
        return [Booking(row) for row in cursor.fetchall()]

    def create_user(self, info: dict[str, Any]):
        role = info.get("role", "customer")
        username = f"({info["firstname"]} {info["lastname"]})"
        try:
            logger.info(f"Adding new user {username} to database …")
            self.execute("""
                     INSERT INTO users (
                                role, firstname, lastname, dob,
                                phonenum, email, password)
                     VALUES (?, ?, ?, ?, ?, ?, ?)
                     """, (
                                role, info["firstname"], info["lastname"],
                                info["dob"], info["phonenum"],
                                info["email"], info["password"],)
            )
        except sqlite3.Error as e:
            logger.exception(f"Failed to add user {username} to database: {e}")
            raise
    def create_driver_application(self, info: dict[str, Any]):
        try:
            self.execute("""
                    INSERT INTO driver_applications (
                                user_id, car_make, car_model,
                                car_colour, man_year, plate_num,
                                status, submitted_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                    info["user_id"], info["car_make"], info["car_model"],
                    info["car_colour"], info["man_year"], info["plate_num"],
                    info["status"],info["submitted_at"],)
            )
        except sqlite3.Error as e:
            logger.exception(f"Failed to submit driver application "
                             f"for user {info['user_id']}: {e}")
            raise

    def update_user(self, user_id, new_attr: dict[str, Any]):
        # Return concatenated str of placeholders. (ie, firstname = ?, dob = ?)
        fields = ', '.join(f"{field} = ?" for field in new_attr.keys())
        params = tuple(new_attr.values()) + (user_id,)
        try:
            self.execute(f"UPDATE user SET {fields} WHERE id = ?", params)
        except sqlite3.Error as e:
            logger.exception(f"Failed to update user ({user_id}) within database: {e}")
            raise

    def create_booking(self, info: dict[str, Any]):

        # Append default data if booking is confirmed.
        driver_id = info.get("driver_id", None)
        status = info.get("status", "waiting_for_assignment")

        try:
            self.execute("""
                    INSERT INTO bookings (
                                customer_id, driver_id, dropoff, 
                                pickup, date, time, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?) 
                    """, (
                    info["customer_id"], driver_id, info["dropoff"],
                    info["pickup"], info["date"], info["time"], status,)
            )
        except sqlite3.Error as e:
            logger.exception(f"Failed to make booking for user ({info['customer_id']}): {e}")
            raise

    def save_address(self, address: dict[str, Any]):
        try:
            self.execute("""
            INSERT INTO addresses (
                customer_id, name, physical_address) 
            VALUES (?, ?, ?)
                        """, (
                address["customer_id"],
                address["name"],
                address["physical_address"],)
            )
        except sqlite3.Error as e:
            logger.exception(f"Failed to add address for user ({address['customer_id']}): {e}")
            raise