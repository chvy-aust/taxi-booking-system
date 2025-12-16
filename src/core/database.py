import logging
import sqlite3
from typing import Any

from src.core.models import User, Booking
from src.utils.constants import DB_FILE, ACTIVE_BOOKING_STATUS, NON_ACTIVE_BOOKING_STATUS

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
        conditions, params = [], ()

        # Checks for optional conditions (ie, email="customer_123@gmail.com")
        if kwargs:
            # Create formatted placeholders (ie, role IN (?, ?).
            for column, values in kwargs.items():
                if not isinstance(values, (tuple, list)):
                    values = (values,)
                placeholders = ', '.join("?" * len(values))
                conditions.append(f"{column} IN ({placeholders})")
                params += tuple(values)
            # Concatenate to WHERE statement.
            sql += f" WHERE " + ' AND '.join(conditions)
        try:
            cursor = self.execute(sql, params)
            return [User(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(
                msg=f"Failed to lookup user table.",
                exc_info=e
            )
            raise

    def fetch_bookings(self, **kwargs) -> list[Booking]:
        """
        Return a list of queried booking instances.
        Accepts optional keyword arguments for filtering.
        """
        sql = "SELECT * FROM bookings"
        conditions, params = [], ()

        # Checks for optional conditions (ie, status="pending")
        if kwargs:
            for column, values in kwargs.items():
                # Create formatted placeholders (ie, status IN (?, ?))
                if not isinstance(values, (tuple, list)):
                    values = (values,)
                placeholders = ', '.join("?" * len(values))
                conditions.append(f"{column} IN ({placeholders})")
                params += tuple(values)
            # (ie, WHERE driver_id IN (?) AND status IN (?, ?))
            sql += " WHERE " + ' AND '.join(conditions)
        sql += " ORDER BY date, time"

        try:
            cursor = self.execute(sql, params)
            return [Booking(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(
                msg=f"Failed to fetch bookings.",
                exc_info=e
            )
            raise

    def create_user(self, info: dict[str, Any]):
        """
        Insert a user record into the database.
        Defaults user role to customer, if not provided.
        """
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
                                info["email"], info["password"])
            )
        except sqlite3.Error as e:
            logger.error(
                msg=f"Failed to add user {username} to database.",
                exc_info=e
            )
            raise

    def create_driver_application(self, info: dict[str, Any]):
        """Insert driver application to the database."""
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
                    info["status"], info["submitted_at"])
            )
        except sqlite3.Error as e:
            logger.error(
                msg=f"Failed to submit driver application for user {info['user_id']}.",
                exc_info=e
            )
            raise

    def update_user(self, user_id, new_attr: dict[str, Any]):
        """
        Update user record within the database.
        Example of new_attr arg: {'firstname':'John', 'lastname':'Doe'}
        """
        # Return concatenated str of placeholders. (ie, firstname = ?, dob = ?)
        fields = ', '.join(f"{field} = ?" for field in new_attr.keys())
        params = tuple(new_attr.values()) + (user_id,)
        try:
            self.execute(f"UPDATE users SET {fields} WHERE id = ?", params)
        except sqlite3.Error as e:
            logger.error(
                msg=f"Failed to update user ({user_id}) within database.",
                exc_info=e
            )
            raise

    def create_booking(self, info: dict[str, Any]):
        """
        Insert new booking record to the database.
        Defaults null driver and booking status to waiting_for_assignment.
        """
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
                    info["pickup"], info["date"], info["time"], status)
            )
        except sqlite3.Error as e:
            logger.error(
                msg=f"Failed to make booking for user ({info['customer_id']}).",
                exc_info=e
            )
            raise

    def save_address(self, address: dict[str, Any]):
        """Insert address record into database."""
        try:
            self.execute("""
            INSERT INTO addresses (
                customer_id, name, physical_address) 
            VALUES (?, ?, ?)
                        """, (
                address["customer_id"],
                address["name"],
                address["physical_address"])
            )
        except sqlite3.Error as e:
            logger.error(
                msg=f"Failed to add address for user ({address['customer_id']}).",
                exc_info=e
            )
            raise

    def update_booking_status(self, booking_id, status):
        """
        Modify the status of an active booking within the database.
        Throw an error if booking is non-active.
        """
        booking = self.fetch_bookings(id=booking_id)[0]
        if booking.status in NON_ACTIVE_BOOKING_STATUS:
            raise sqlite3.Error("Cannot modify a non-active booking.")

        try:
            self.execute("""
                UPDATE bookings
                SET status = ?
                WHERE id = ?
                """, (status, booking_id))
        except  sqlite3.Error as e:
            logger.error(
                msg=f"Failed to change booking ({booking_id}) status to {status}.",
                exc_info=e
            )
            raise

    def is_driver_available(self, driver_id) -> bool:
        """Return False if driver has any unfinished bookings, else True."""
        active_bookings = self.fetch_bookings(
                driver_id=driver_id, status=ACTIVE_BOOKING_STATUS)
        return False if active_bookings else True

    def assign_booking_driver(self, booking_id, driver_id):
        """
        Attach driver_id to booking waiting for assignment.
        Throw an error if the driver is assigned to an active booking.
        """
        try:
            if not self.is_driver_available(driver_id):
                raise sqlite3.Error(f"This driver ({driver_id}) is currently busy.")

            self.execute("""
                UPDATE bookings
                SET driver_id = ?
                WHERE id = ?
            """, (driver_id, booking_id))

        except sqlite3.Error as e:
            logger.error(
                msg=f"Failed to assign driver ({driver_id}) to booking ({booking_id}).",
                exc_info=e
            )
            raise
