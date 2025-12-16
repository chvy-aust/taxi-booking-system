import datetime
import logging
import random
import sqlite3

from faker import Faker

from src.core.database import DatabaseConnection
from src.utils.constants import NON_ACTIVE_BOOKING_STATUS

faker = Faker()
logger = logging.getLogger(__name__)

def generate_users() -> list[dict]:
    """Create 2 predefined customers, admins and drivers and other,
    fully-randomized accounts."""
    users = [
        {"role": "customer", "email": "customer_123@gmail.com"},
        {"role": "customer", "email": "ran_customer1@gmail.com"},
        {"role": "driver", "email": "driver_123@gmail.com"},
        {"role": "driver", "email": "ran_driver1@gmail.com"},
        {"role": "admin", "email": "admin_123@gmail.com"},
        {"role": "admin", "email": "ran_admin1@gmail.com"}
    ]

    for user in users:
        # Append randomized data to pre- defined users.
        user.update({
            "firstname": faker.first_name(),
            "lastname": faker.last_name(),
            "dob": faker.date_of_birth(minimum_age=18),
            "phonenum": faker.numerify("868 ### ####"),
            "password": "Pass123**"
        })

    for role, amount in {'customer': 25, 'driver': 8, 'admin': 4}.items():
        # Add fully-randomized users to sample pool.
        users += [{
                "role": role,
                "firstname": faker.first_name(),
                "lastname": faker.last_name(),
                "dob": faker.date_of_birth(minimum_age=18),
                "phonenum": faker.numerify("868 ### ####"),
                "email": faker.unique.email(),
                "password": faker.password(8)
        } for _ in range(amount)]
    return users

def fetch_db_sample_users() -> dict[str, list]:
    """Return a collection of generated users from the database."""
    try:
        with DatabaseConnection() as conn:
            sample_users = {
                "customers": conn.fetch_users(role="customer"),
                "drivers": conn.fetch_users(role="driver"),
                "admins": conn.fetch_users(role="admin")
            }
    except sqlite3.Error as e:
        logger.error(
            msg="Failed to retrieve sample users during booking generation.",
            exc_info=e
        )
    return sample_users

def generate_bookings() -> list[dict]:
    PREDEFINED_EMAILS = (
        "customer_123@gmail.com",
        "ran_customer1@gmail.com",
        "driver_123@gmail.com"
    )

    users = fetch_db_sample_users()

    # Store pre-defined email to user mapping for testing.
    testing_users = {
        user.email: user for user in users["customers"] + users["drivers"]
        if user.email in PREDEFINED_EMAILS
    }

    bookings = [{
        "customer_id": customer.id,
        "driver_id": random.choice(users["drivers"]).id,
        "dropoff": faker.address(),
        "pickup": faker.address(),
        "date": str(faker.date_between(start_date="-300d", end_date="-2d")),
        "time": faker.date_time().strftime("%H:%M:%S"),
        "status": random.choice(NON_ACTIVE_BOOKING_STATUS)
        # Generate 1-5 past bookings for each customer
         } for _ in range(random.randint(1,6))
        for customer in users["customers"]]

    # Generate active bookings for testing
    bookings += [{
        "customer_id": testing_users["customer_123@gmail.com"].id,
        "driver_id": testing_users["driver_123@gmail.com"].id,
        "dropoff": faker.address(),
        "pickup": faker.address(),
        "date": str(datetime.date.today()),
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "status": "waiting_for_pickup"
    },{
        "customer_id": testing_users["ran_customer1@gmail.com"].id,
        "dropoff": faker.address(),
        "pickup": faker.address(),
        "date": str(datetime.date.today()),
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "status": "waiting_for_assignment" }]

    return bookings

def seed_database():

    logger.info("Seeding Database …")
    try:
        # Must commit users records prior to bookings.
        with DatabaseConnection() as conn:
            generated_users = generate_users()
            for user in generated_users:
                conn.create_user(user)
        # Bookings contain user dependencies that must be committed.
        with DatabaseConnection() as conn:
            bookings = generate_bookings()
            for booking in bookings:
                conn.create_booking(booking)
    except sqlite3.Error as e:
        logger.error(
            msg="Something unexpected occurred while generating users.",
            exc_info=e
        )
        raise
    else:
        logger.info("Database successfully seeded … [ ✔ ]")
        logger.info("For more information concerning seeding, see README.md")

if __name__ == "__main__":
    seed_database()