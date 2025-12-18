import re

from PyQt6.QtCore import QDate

from src.widgets import InputEdit


EMAIL_PATTERN = re.compile(r"^[\w\-.]+@([\w-]+\.)+[\w-]{2,}$")
PASSWORD_PATTERN = re.compile(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}")
# PREVIOUSLY USED PHONENUM REGEX
# PHONENUM_PATTERN = re.compile(r"^\d{3}[-\s]?\d{3}[-\s]?\d{4}$")

def validate_phonenum(phonenum: str) -> bool:
    """
    Check if phone number matches required format.
    Pattern: Optional '+', then only digits and spaces.
    """
    # Trim first occurrence of optional '+'.
    if phonenum.startswith('+'):
        phonenum = phonenum[1:]

    if phonenum == "":
        return False

    # Check against strings ending in non-digits.
    if not phonenum[-1].isdigit():
        return False

    digit_count = 0
    for char in phonenum:
        if char.isdigit():
            digit_count += 1
        # Check against non-space, non-digit characters.
        elif not char.isspace():
            return False
    return 7 <= digit_count <= 15





AGE_REQUIREMENT = 18


def validate_password(password: str) -> bool:
    """Check if password matches required format."""
    if password == "":
        return False
    return bool(re.match(PASSWORD_PATTERN, password))


def validate_dob(dob: QDate) -> bool:
    """Check whether date of birth meets the age requirement."""
    # Get current date
    today = QDate.currentDate()
    # Calculate user age, not considering if their birthday passed.
    age = today.year() - dob.year()
    # If user's birthday has not passed, subtract a year.
    if [today.month(), today.day()] < [dob.month(), dob.day()]:
        age -= 1
    return age >= AGE_REQUIREMENT



def validate_email(email: str) -> bool:
    """Return True if email matches format and is not null, else False."""
    if email == "":
        return False
    return bool(re.match(EMAIL_PATTERN, email))


def is_email_unique(email: str) -> bool:
    """Return False if any user is attached to email, else True."""
    from src.core.database import DatabaseConnection
    with DatabaseConnection() as conn:
        user = conn.fetch_users(email=email)
        return not bool(user)


def is_fields_valid(fields: dict[InputEdit, bool]) -> bool:
    """
    Check the validity of a given InputEdit fields + clear/show errors.
    Return a bool indicator of whether all fields are valid.
    """
    for field in fields.keys():
        field.clear_error()
    flag = True
    for field, is_valid in fields.items():
        if not is_valid:
            field.show_error()
            flag = False
    return flag

