import sqlite3

from database.db import DatabaseConnection


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

    def cancel(self):
        try:
            with DatabaseConnection() as conn:
                conn.execute("""
                UPDATE booking
                SET status = ?
                WHERE id = ?
                """, ("cancelled", self.id))
        except sqlite3.Error as e:
            print(f"( WARNING ⚠ ) ERROR: {e}")
            raise
        else:
            # Update the booking instance.
            setattr(self, "status", "cancelled")

    def __str__(self):
        string = f":: {self.date} - {self.time}"
        string += f" | STATUS: {self.status.replace("_", " ".capitalize())}"
        return string
