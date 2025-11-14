"""
A helper package for field validation.

Provides:
    - Null field check.
    - Age requirement check.
    - Match check between created and confirmed passwords.
"""
import re
from datetime import date

from PyQt6.QtCore import QDate

from src.app.widgets.input_edit import InputEdit

PHONENUM_PATTERN = re.compile(r"(^\+?\d{1,3}[-\s]?)?(\(\d{1,3}\)|\d{1,3})[-\s]?\d{1,3}[-\s]?\d{1,4}$")
EMAIL_PATTERN = re.compile(r"^[\w\-.]+@([\w-]+\.)+[\w-]{2,4}$")
PASSWORD_PATTERN = re.compile(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}")

def validate_null(credentials: dict[InputEdit, str]) -> bool:
    """
    Return bool flag indicating present null fields.
    Accepts dictionary containing instances and values for fields.
    """
    flag = True
    # Check for null fields.
    for field, value in credentials.items():
        if value == "":
            field.show_error()
            flag = False
    return flag

def validate_age(dob: QDate):
    today = date.today()
    age = today.year - dob.year()
    if [today.month, today.day] > [dob.month(), dob.year()]:
        age -= 1
    return age >= 18

def validate_phonenum(phonenum):
    return re.match(PHONENUM_PATTERN, phonenum)

def validate_email(email):
    return re.match(EMAIL_PATTERN, email)