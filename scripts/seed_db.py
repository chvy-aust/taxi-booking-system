import logging
import random
import sqlite3

from faker import Faker

from src.core.database import DatabaseConnection

faker = Faker()
logger = logging.getLogger(__name__)
def generate_users():
    sample_users = [
             {"role": "customer", "email": "customer_123@gmail.com"},
             {"role": "customer", "email": "ran_customer1@gmail.com"},
             {"role": "driver", "email": "driver_123@gmail.com"},
             {"role": "driver", "email": "ran_driver1@gmail.com"},
             {"role": "admin", "email": "admin_123@gmail.com"},
             {"role": "admin", "email": "ran_admin1@gmail.com"}
    ]

    for user in sample_users:
        # Generate generic information for test users.
        user["firstname"] = faker.first_name()
        user["lastname"] = faker.last_name()
        user["dob"] = faker.date_of_birth(minimum_age=18).strftime("yyyy-MM-dd")
        user["phonenum"] = faker.numerify("868 ### ####")
        user["password"] = "Pass123**"

    for role, amount in {'customer': 25, 'driver': 8, 'admin': 4}.items():
        # Generate additional full sample users.
        sample_users += [{
                "role": role,
                "firstname": faker.first_name(),
                "lastname": faker.last_name(),
                "dob": faker.date_of_birth(minimum_age=18).strftime("yyyy-MM-dd"),
                "phonenum": faker.phone_number(),
                "email": faker.email(),
                "password": faker.password(8)
        } for _ in range(amount)]

    return sample_users


def generate_bookings(generated_users):
    sample_bookings, customers, drivers = [], [], []
    try:
        with DatabaseConnection() as conn:
            users = [conn.lookup_user(user["email"] for user in generated_users)]
            for user in users:
                if user.role == "customer":
                    customers += user
                if user.role == "driver":
                    drivers += user
    except sqlite3.Error as e:
        logger.exception(e)



def seed_database():

    logger.info("Seeding Database …")
    try:
        with DatabaseConnection() as conn:
            logger.info("❯❯ Attempting to generate user data … [ ]")
            generated_users = generate_users()
            for generated_user in generated_users:
                conn.create_user(generated_user)
            logger.info("❯❯ User data generated … [ ✔ ]")
            logger.info("❯❯ Attempting to generate booking data … [ ]")
            # db method goes here
            # logger.info("❯❯ Booking data generated … [ ✔ ]")
            logger.info("❯❯ Data successfully generated [ ✔ ]")
    except sqlite3.Error as e:
        logger.exception(e)
        raise
    else:
        logger.info("Successfully seeded database!")
