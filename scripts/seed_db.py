import datetime
import logging
import random
import sqlite3

from faker import Faker

from src.core.database import DatabaseConnection

faker = Faker()
logger = logging.getLogger(__name__)
def generate_users():
    users = [
             {"role": "customer", "email": "customer_123@gmail.com"},
             {"role": "customer", "email": "ran_customer1@gmail.com"},
             {"role": "driver", "email": "driver_123@gmail.com"},
             {"role": "driver", "email": "ran_driver1@gmail.com"},
             {"role": "admin", "email": "admin_123@gmail.com"},
             {"role": "admin", "email": "ran_admin1@gmail.com"}
    ]

    for user in users:
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
        users += [{
                "role": role,
                "firstname": faker.first_name(),
                "lastname": faker.last_name(),
                "dob": faker.date_of_birth(minimum_age=18),
                "phonenum": faker.numerify("868 ### ####"),
                "email": faker.email(),
                "password": faker.password(8)
        } for _ in range(amount)]

    return users


def generate_bookings(generated_users):

    try:
        with DatabaseConnection() as conn:
            customers, drivers = [], []
            for user in generated_users:
                if user["role"] == "customer":
                    customers.extend(conn.fetch_users(email=user["email"]))
                elif user["role"] == "driver":
                    drivers.extend(conn.fetch_users(email=user["email"]))
    except sqlite3.Error as e:
        logger.exception(e)

    testing_drivers, driver_ids = [], []
    # Collect testing driver ids + all driver ids.
    for driver in drivers:
        if driver.email in ("driver_123@gmail.com", "ran_driver1@gmail.com"):
            testing_drivers.append(driver)
        driver_ids.append(driver.id)
    # Collect testing customers
    testing_customers = [customer for customer in customers
                        if customer.email in (
                                 "customer_123@gmail.com",
                                 "ran_customer1@gmail.com")]

    # Define range of booking dates.
    end_date = datetime.date.today() - datetime.timedelta(days=1)
    start_date = end_date - datetime.timedelta(days=365)

    past_bookings = []
    # Generates past bookings
    for customer in customers:
        for _ in range(random.randint(3, 10)):
            past_bookings.append({
                "customer_id": customer.id,
                "driver_id": random.choice(driver_ids),
                "dropoff": faker.address(),
                "pickup": faker.address(),
                "date": str(faker.date_between_dates(start_date, end_date)),
                "time": faker.time(),
                "status": random.choice(["cancelled", "completed"])
            })

    active_bookings = []
    # Generates active bookings for testing customers + drivers
    for customer, driver in zip(testing_customers, testing_drivers):
        active_bookings.append({
            "customer_id": customer.id,
            "driver_id": driver.id,
            "dropoff": faker.address(),
            "pickup": faker.address(),
            "date": str(datetime.date.today()),
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "status": "waiting_for_pickup"
        })

    return [active_bookings, past_bookings]

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
            bookings = generate_bookings(generated_users)
            print(bookings)
            for booking_set in bookings:
                for booking in booking_set:
                    conn.create_booking(booking)
    except sqlite3.Error as e:
        logger.exception(f"An exception occurred during booking seeding: {e}")
        raise
    else:
        logger.info("❯❯ Booking data generated … [ ✔ ]")

