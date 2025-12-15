import datetime
import logging
import random
import sqlite3

from faker import Faker

from src.core.database import DatabaseConnection

faker = Faker()
logger = logging.getLogger(__name__)
TESTING_CUSTOMERS = [
        {"role": "customer", "email": "customer_123@gmail.com"},
        {"role": "customer", "email": "ran_customer1@gmail.com"},
]
TESTING_DRIVERS = [
        {"role": "driver", "email": "driver_123@gmail.com"},
        {"role": "driver", "email": "ran_driver1@gmail.com"},
]

TESTING_ADMINS = [
        {"role": "admin", "email": "admin_123@gmail.com"},
        {"role": "admin", "email": "ran_admin1@gmail.com"}
]

testing_users = TESTING_CUSTOMERS + TESTING_DRIVERS + TESTING_ADMINS
random_users = []
def generate_users():

    for user in testing_users:
        # Generate generic information for test users.
        user.update({
            "firstname": faker.first_name(),
            "lastname": faker.last_name(),
            "dob": faker.date_of_birth(minimum_age=18),
            "phonenum": faker.numerify("868 ### ####"),
            "password": "Pass123**"
        })

    for role, amount in {'customer': 25, 'driver': 8, 'admin': 4}.items():
        # Generate additional full sample users.
        random_users.extend({
                "role": role,
                "firstname": faker.first_name(),
                "lastname": faker.last_name(),
                "dob": faker.date_of_birth(minimum_age=18),
                "phonenum": faker.numerify("868 ### ####"),
                "email": faker.unique.email(),
                "password": faker.password(8)
        } for _ in range(amount))

    return testing_users + random_users

def generate_bookings():
    try:
        with DatabaseConnection() as conn:
            customers = conn.fetch_users(role="customer")
            drivers = conn.fetch_users(role="driver")
    except sqlite3.Error as e:
        logger.exception(e)

    testing_customers, random_customers = {}, []
    for customer in customers:
        if customer.email in ("customer_123@gmail.com","ran_customer1@gmail.com"):
            testing_customers[customer.email] = customer

    testing_drivers, random_drivers = {}, []
    for driver in drivers:
        if driver.email in ("driver_123@gmail.com", "ran_driver1@gmail.com"):
            testing_drivers[driver.email] = driver

    past_bookings = []
    # Generates past bookings
    for customer in customers:
        for _ in range(random.randint(1,16)):
            past_bookings.append({
            "customer_id": customer.id,
            "driver_id": random.choice(drivers).id,
            "dropoff": faker.address(),
            "pickup": faker.address(),
            "date": str(faker.date_between(start_date="-300d", end_date="-2d")),
            "time": faker.date_time().strftime("%H:%M:%S"),
            "status": random.choice(["cancelled", "completed"])
        })

    wfp_booking = [{
        "customer_id": testing_customers["customer_123@gmail.com"].id,
        "driver_id": testing_drivers["driver_123@gmail.com"].id,
        "dropoff": faker.address(),
        "pickup": faker.address(),
        "date": str(datetime.date.today()),
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "status": "waiting_for_pickup"
    }]

    tba_booking = [{
        "customer_id": testing_customers["ran_customer1@gmail.com"].id,
        "dropoff": faker.address(),
        "pickup": faker.address(),
        "date": str(datetime.date.today()),
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "status": "waiting_for_assignment"
    }]

    return [past_bookings, tba_booking, wfp_booking]

def seed_database():

    logger.info("Seeding Database …")
    try:
        with DatabaseConnection() as conn:
            logger.info("❯❯ Attempting to generate user data … [ ]")
            generated_users = generate_users()
            for user in generated_users:
                conn.create_user(user)

    except sqlite3.Error as e:
        logger.exception(f"An exception occurred during user seeding: {e}")
        raise
    else:
        logger.info("❯❯ User data generated … [ ✔ ]")

    try:
        with DatabaseConnection() as conn:
            logger.info("❯❯ Attempting to generate booking data … [ ]")
            bookings = generate_bookings()
            for booking_set in bookings:
                for booking in booking_set:
                    conn.create_booking(booking)
    except sqlite3.Error as e:
        logger.exception(f"An exception occurred during booking seeding: {e}")
        raise
    else:
        logger.info("❯❯ Booking data generated … [ ✔ ]")

