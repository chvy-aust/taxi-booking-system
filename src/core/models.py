import logging
import sqlite3
from typing import Any

logger = logging.getLogger(__name__)
class User:
    def __init__(self, row):
        self.id = row['id']
        self.role = row['role']
        self.firstname = row['firstname']
        self.lastname = row['lastname']
        self.dob = row['dob']
        self.phonenum = row['phonenum']
        self.email = row['email']
        self.password = row['password']

    @property
    def fullname(self):
        return f"{self.firstname} {self.lastname}"

    def update(self, new_attr: dict[str, Any]):
        """
        Update user record in database and the user instance.
        Accepts a dictionary of str attributes and their new values.
        """
        if new_attr is None:
            return

        # Update the user record in db.
        from src.core.database import DatabaseConnection
        with DatabaseConnection() as conn:
             conn.update_user(self.id, new_attr)

        # Update the user instance.
        for attribute, value in new_attr.items():
            setattr(self, attribute, value)

    def compare_attr(self, attr: dict[str, Any]):
        """Return a dict containing new user values."""
        new_attr = {}
        # Check if credential is != current user credential.
        for key, value in attr.items():
            # Collect any updated credential
            if hasattr(self, key):
                if value != getattr(self, key):
                    new_attr[key] = value
        return new_attr

class Booking:
    def __init__(self, row_object):
        self.id = row_object["id"]
        self.customer_id = row_object["customer_id"]
        self.driver_id = row_object["driver_id"]
        self.dropoff = row_object["dropoff"]
        self.pickup = row_object["pickup"]
        self.date = row_object["date"]
        self.time = row_object["time"]
        self.status = row_object["status"]

    def update_status(self, status):
        if self.status == "cancelled":
            raise sqlite3.Error("Cannot modify a cancelled booking.")

        from src.core.database import DatabaseConnection
        with DatabaseConnection() as conn:
            conn.change_booking_status(self.id, status)
        self.status = status

    @property
    def customer(self):
        from src.core.database import DatabaseConnection
        with DatabaseConnection() as conn:
            return conn.fetch_users(id=self.customer_id)[0]

    @property
    def get_driver(self):
        from src.core.database import DatabaseConnection
        with DatabaseConnection() as conn:
            return conn.fetch_users(id=self.driver_id)[0] or None


    def __str__(self):
        string = f":: {self.date} - {self.time}"
        string += f" | STATUS: {self.status.replace("_", " ".capitalize())}"
        return string
