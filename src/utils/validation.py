import re

from PyQt6.QtCore import QDate

PHONENUM_PATTERN = re.compile(r"(^\+\d{1,3}[-\s])?\d{1,3}[-\s]?\d{1,3}[-\s]?\d{1,4}$")
EMAIL_PATTERN = re.compile(r"^[\w\-.]+@([\w-]+\.)+[\w-]{2,4}$")
PASSWORD_PATTERN = re.compile(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}")
AGE_REQUIREMENT = 18

def validate_password(password: str) -> bool:
    """Return if password matches required format."""
    if password == "":
        return False
    return bool(re.match(PASSWORD_PATTERN, password))


def validate_dob(dob: QDate) -> bool:
    """Indicate whether date of birth meets the age requirement."""
    # Get current date
    today = QDate.currentDate()
    # Calculate user age, not considering if their birthday passed.
    age = today.year() - dob.year()
    # If user's birthday has not passed, subtract a year.
    if [today.month(), today.day()] > [dob.month(), dob.day()]:
        age -= 1
    return bool(age >= AGE_REQUIREMENT)


def validate_phonenum(phonenum: str) -> bool:
    """Return if password matches required format."""
    if phonenum == "":
        return False
    return bool(re.match(PHONENUM_PATTERN, phonenum))


def validate_email(email: str) -> bool:
    """Return if email matches required format."""
    if email == "":
        return False
    return bool(re.match(EMAIL_PATTERN, email))


