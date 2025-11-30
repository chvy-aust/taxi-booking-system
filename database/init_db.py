import sqlite3

from database.db import DatabaseConnection

USER_SCHEMA = """
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
    print("( ℹ ) Initializing Database …")
    try:
        with DatabaseConnection() as cursor:
            print("❯❯ Attempting to create tables … [ ]")
            cursor.execute(USER_SCHEMA)
            cursor.execute(BOOKING_SCHEMA)
            print("❯❯ Tables successfully created [ ✔ ]")
            # Other executions here
            # Eg. Creating indexes, creating triggers, etc

    except sqlite3.Error as e:
        print(f"( CRITICAL ⚠ ) Failed to initialize database! ERROR: {e}")
        raise
    else:
        print("( ℹ ) Database successfully created !")

if __name__ == "__main__":
    initialize_database()
