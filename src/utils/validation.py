import re

from PyQt6.QtCore import QDate


class Validator:
    PHONENUM_PATTERN = re.compile(r"(^\+\d{1,3}[-\s])?\d{1,3}[-\s]?\d{1,3}[-\s]?\d{1,4}$")
    EMAIL_PATTERN = re.compile(r"^[\w\-.]+@([\w-]+\.)+[\w-]{2,4}$")
    PASSWORD_PATTERN = re.compile(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}")
    AGE_REQUIREMENT = 18

    @staticmethod
    def firstname_check(firstname: str) -> bool:
        """Indicate whether firstname is null."""
        return firstname == ""

    @staticmethod
    def lastname_check(lastname: str) -> bool:
        """Indicate whether lastname is null."""
        return lastname == ""

    @classmethod
    def dob_check(cls, dob: QDate) -> bool:
        """Indicate whether date of birth meets the age requirement."""
        today = QDate.currentDate()
        age = today.year() - dob.year()
        if [today.month(), today.day()] > [dob.month(), dob.day()]:
            age -= 1
        return bool(age >= cls.AGE_REQUIREMENT)

    @classmethod
    def phonenum_check(cls, phonenum: str) -> bool:
        """Return if password matches required format."""
        if phonenum == "":
            return False
        return bool(re.match(cls.PHONENUM_PATTERN, phonenum))

    @classmethod
    def email_check(cls, email: str) -> bool:
        """Return if email matches required format."""
        if email == "":
            return False
        return bool(re.match(cls.EMAIL_PATTERN, email))

    @classmethod
    def password_check(cls, password: str) -> bool:
        """Return if password matches required format."""
        if password == "":
            return False
        return bool(re.match(cls.PASSWORD_PATTERN, password))

    @staticmethod
    def match_passwords(created_pass: str, confirmed_pass: str) -> bool:
        return created_pass == confirmed_pass

