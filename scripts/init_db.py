import logging
import sqlite3

from src.core.database import DatabaseConnection



USERS_SCHEMA = """
    CREATE TABLE IF NOT EXISTS users (
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
        customer_id INT NOT NULL REFERENCES users(id),
        name TEXT NOT NULL,
        physical_address TEXT NOT NULL
    )
"""

DRIVER_SCHEMA = """
    CREATE TABLE IF NOT EXISTS drivers (
        id INTEGER PRIMARY KEY REFERENCES users(id), 
        car_make TEXT NOT NULL,
        car_model TEXT NOT NULL,
        car_colour TEXT NOT NULL,
        man_year INT NOT NULL,
        plate_num TEXT NOT NULL,
        is_online BOOLEAN NOT NULL DEFAULT FALSE
    )
"""

DRIVER_APPLICATION_SCHEMA = """
    CREATE TABLE IF NOT EXISTS driver_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    user_id INT NOT NULL REFERENCES users(id),
    car_make TEXT NOT NULL,
    car_model TEXT NOT NULL,
    car_colour TEXT NOT NULL,
    man_year INT NOT NULL,
    plate_num TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending' CHECK ( 
        status IN('pending', 'approved', 'rejected')),
    submitted_at TEXT NOT NULL,
    reviewed_at TEXT NULL,
    reviewed_by INT NULL REFERENCES users(id),
    review_comment TEXT NULL
    )
"""

BOOKINGS_SCHEMA = """
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INT NOT NULL REFERENCES users(id),
        driver_id INT NULL REFERENCES users(id),
        dropoff TEXT NOT NULL,
        pickup TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'waiting_for_assignment' CHECK(
            status IN('waiting_for_assignment', 'waiting_for_pickup', 
                      'in_process', 'completed', 'cancelled'))
    )
"""

def initialize_database():
    logger = logging.getLogger(__name__)
    logger.info("Initializing Database …")
    try:
        with DatabaseConnection() as cursor:
            logger.info("Attempting to create tables … [  ]")
            cursor.execute(USERS_SCHEMA)
            cursor.execute(BOOKINGS_SCHEMA)
            cursor.execute(ADDRESSES_SCHEMA)
            cursor.execute(DRIVER_SCHEMA)
            cursor.execute(DRIVER_APPLICATION_SCHEMA)
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