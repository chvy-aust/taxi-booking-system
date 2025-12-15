import logging
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

        from src.core.database import DatabaseConnection
        with DatabaseConnection() as conn:
             conn.update_user(self.id, new_attr)

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
    formatted_status = {
        "waiting_for_assignment": "Waiting for Driver Assignment",
        "waiting_for_pickup": "Pickup in Process",
        "in_process": "Drop off in Process",
        "completed": "Booking Completed",
        "cancelled": "This booking was cancelled."
    }

    next_status = {
        "waiting_for_assignment": "waiting_for_pickup",
        "waiting_for_pickup": "in_process",
        "in_process": "completed"
    }

    def __init__(self, row):
        self.id = row["id"]
        self.customer_id = row["customer_id"]
        self.driver_id = row["driver_id"]
        self.dropoff = row["dropoff"]
        self.pickup = row["pickup"]
        self.date = row["date"]
        self.time = row["time"]
        self.status = row["status"]

    def update_status(self):
        """
        Progress the status of an active booking.
        Get the next booking phase based on the current status.
        """

        new_status = self.next_status.get(self.status)
        # Update booking instance and db record.
        from src.core.database import DatabaseConnection
        with DatabaseConnection() as conn:
            conn.update_booking_status(
                booking_id=self.id,
                status=new_status)
        self.status = new_status

    def assign_driver(self, driver_id):
        """Assign an available driver to the current booking."""
        from src.core.database import DatabaseConnection
        with DatabaseConnection() as conn:
            conn.assign_booking_driver(
                booking_id=self.id,
                driver_id=driver_id)
        self.driver_id = driver_id


    def cancel(self):
        """Cancel the booking instance and db record."""
        from src.core.database import DatabaseConnection
        with DatabaseConnection() as conn:
            conn.update_booking_status(
                booking_id=self.id,
                status="cancelled")
        self.status = "cancelled"

    @property
    def get_formatted_status(self):
        return self.formatted_status.get(self.status)

    @property
    def customer(self) -> User:
        """Return the customer attached to the booking."""
        from src.core.database import DatabaseConnection
        with DatabaseConnection() as conn:
            return conn.fetch_users(id=self.customer_id)[0]

    @property
    def driver(self) -> User:
        """Return the driver assigned to the booking."""
        from src.core.database import DatabaseConnection
        with DatabaseConnection() as conn:
            drivers = conn.fetch_users(id=self.driver_id)
            return drivers[0] if drivers else None

