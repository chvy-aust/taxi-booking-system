import logging
import sqlite3

from src.core.database import DatabaseConnection



USER_SCHEMA = """
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        dob TEXT NOT NULL,
        phonenum TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """

ADDRESSES_SCHEMA = """
    CREATE TABLE IF NOT EXISTS addresses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INT NOT NULL REFERENCES user(id),
        name TEXT NOT NULL,
        physical_address TEXT NOT NULL
    )
"""

DRIVER_PROFILE_SCHEMA = """
    CREATE TABLE IF NOT EXISTS driver_profile (
        id INTEGER PRIMARY KEY REFERENCES user(id), 
        car_make TEXT NOT NULL,
        car_color TEXT NOT NULL,
        plate_num TEXT NOT NULL
    )
"""


BOOKING_SCHEMA = """
    CREATE TABLE IF NOT EXISTS booking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INT NOT NULL REFERENCES user(id),
        driver_id INT NULL REFERENCES user(id),
        dropoff TEXT NOT NULL,
        pickup TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'waiting_for_assignment' CHECK(
            status IN('waiting_for_assignment', 'waiting_for_pickup', 'in_process', 'completed', 'cancelled'))
    )
    """

def initialize_database():
    logger = logging.getLogger(__name__)
    logger.info("Initializing Database …")
    try:
        with DatabaseConnection() as cursor:
            logger.info("Attempting to create tables … [  ]")
            cursor.execute(USER_SCHEMA)
            cursor.execute(BOOKING_SCHEMA)
            cursor.execute(ADDRESSES_SCHEMA)
            cursor.execute(DRIVER_PROFILE_SCHEMA)
            logger.info("Tables created successfully … [ ✔ ]")
            # Other executions here
            # Eg. Creating indexes, creating triggers, etc

    except sqlite3.Error as e:
        logger.exception(f"Failed to initialize database: {e}")
        raise
    else:
        logger.info("Database initialized.")


if __name__ == "__main__":
    initialize_database()