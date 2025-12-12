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
        return self.conn.execute(sql, params)


    def fetch_users(self, **kwargs) -> list[User]:
        """
        Return a list of queried user instances.
        Accepts optional keyword arguments for filtering.
        """
        sql = "SELECT * FROM users"
        fields, params = [], ()

        # Checks for optional conditions (ie, email="customer_123@gmail.com")
        if kwargs:
            # Create formatted placeholders (ie, role IN (?, ?).
            for field, values in kwargs.items():
                if not isinstance(values, (tuple, list)):
                    values = (values,)
                placeholders = ', '.join("?" * len(values))
                fields.append(f"{field} IN ({placeholders})")
                params += tuple(values)
            # Concatenate to conditional statement.
            sql += f" WHERE " + ' AND '.join(fields)
        try:
            cursor = self.execute(sql, params)
            return [User(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.exception(f"Failed to lookup user table: {e}")
            raise

    def fetch_bookings(self, **kwargs):
        """
        Return a list of queried booking instances.
        Accepts optional keyword arguments for filtering.
        """
        sql = "SELECT * FROM bookings"
        fields, params = [], ()

        # Checks for optional conditions (ie, status="pending")
        if kwargs:
            for field, values in kwargs.items():
                # Create formatted placeholders (ie, status IN (?, ?))
                if not isinstance(values, (tuple, list)):
                    values = (values,)
                placeholders = ', '.join("?" * len(values))
                fields.append(f"{field} IN ({placeholders})")
                params += tuple(values)
            # Concatenate to conditional statement.
            # (ie, WHERE driver_id IN (?) AND status IN (?, ?))
            sql += f" WHERE " + ' AND '.join(fields)

        try:
            cursor = self.execute(sql, params)
            return [Booking(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.exception(f"Failed to fetch bookings: {e}")
            raise

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
            self.execute(f"UPDATE users SET {fields} WHERE id = ?", params)
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

    def change_booking_status(self, booking_id, status):
        try:
            self.execute("""
                UPDATE bookings
                SET status = ?
                WHERE id = ?
                """, (booking_id, status))
        except  sqlite3.Error as e:
            logger.exception(f"Failed to update status for booking {booking_id} to {status}: {e}")
            raise