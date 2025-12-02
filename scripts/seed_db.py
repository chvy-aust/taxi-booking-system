import sqlite3

from faker import Faker

from src.core.database import DatabaseConnection

faker = Faker()
def generate_users():
    users = [{"id": 110, "role": "customer", "email": "jnjo32@gmail.com", "password": "P@ss123!"},
             {"id": 111, "role": "customer", "email": "ran_cust1@gmail.com", "password": "Cust_m1**!"},
             {"id": 105, "role": "driver", "email": "drv_12@gmail.com", "password": "0Dv32!**"},
             {"id": 106, "role": "driver", "email": "ran_driv1@gmail.com", "password": "Driv_r1**!"},
             {"id": 101, "role": "admin", "email": "drv_12@gmail.com", "password": "0Dv32!**"},
             {"id": 102, "role": "admin", "email": "ran_driv1@gmail.com", "password": "Driv_r1**!"}]

    for user in users:
        user["firstname"] = faker.first_name()
        user["lastname"] = faker.last_name()
        user["dob"] = faker.date_of_birth(minimum_age=18).strftime("yyyy-MM-dd")
        user["phonenum"] = faker.phone_number()

    return users

def generate_bookings():
    return [{"": 1}]

if __name__ == "__main__":
    print("( ℹ ) Seeding Database …")
    try:
        with DatabaseConnection() as conn:
            print("❯❯ Attempting to generate user data … [ ]")
            for user in generate_users():
                conn.create_user(user)
            print("❯❯ User data generated … [ ✔ ]")
            print("❯❯ Attempting to generate booking data … [ ]")
            for booking in generate_bookings():
                conn.create_booking(booking)
            print("❯❯ Booking data generated … [ ✔ ]")
            print("❯❯ Data successfully generated [ ✔ ]")
    except sqlite3.Error as e:
            print(f"( CRITICAL ⚠ ) Failed to seed database! ERROR: {e}")
            raise
    else:
        print("( ℹ ) Database successfully seeded !")
