import sqlite3

from PyQt6.QtWidgets import QLineEdit, QHBoxLayout, QVBoxLayout, QFrame

from src.scenes import BaseScene
from src.utils import validate_phonenum, validate_dob, \
    validate_email, validate_password, is_email_unique
from src.utils.constants import ErrorMessage
from src.widgets import InputEdit, DateEdit

# Str constants for tooltip hinting.
AGE_REQUIREMENT_HINT = "You must be 18+ to use this service."
PHONENUM_FORMAT_HINT = (
        "May contain optional country code. Must have area and local code.\n"
        "Examples of valid formats:\n"
        "+1 (123) 456 7890 | (123) 456 7890\n"
        "1 123 456 7890 | 1-123-456-7890\n"
        "123 456 7890 | 123-456-7890"
    )
EMAIL_FORMAT_HINT = "Must contain '@' and '.'"
PASSWORD_FORMAT_HINT = (
        "Password must contain atleast:\n"
        "   → 8 characters\n"
        "   → 1 uppercase letter\n"
        "   → 1 lowercase letter\n"
        "   → 1 number."
    )
MATCHING_PASSWORD_HINT = "These passwords must match."

class UserForm(QFrame):

    def __init__(self, parent: BaseScene):
        super().__init__(parent)
        self.parent_scene: BaseScene = parent

        # Name fields.
        self.firstname = InputEdit("Enter first name:")
        self.lastname = InputEdit("Enter last name:")
        # Date of birth field + tooltip.
        self.dob = DateEdit("Enter date of birth:")
        self.dob.set_tooltip(AGE_REQUIREMENT_HINT)
        # Phone number field + tooltip.
        self.phonenum = InputEdit("Enter phone number:")
        self.phonenum.set_tooltip(PHONENUM_FORMAT_HINT)
        # Email field + tooltip.
        self.email = InputEdit("Enter email address:")
        self.email.set_tooltip(EMAIL_FORMAT_HINT)
        self.address = InputEdit("Enter home address:")
        # Password fields + tooltips.
        self.create_pass = InputEdit("Create new password:")
        self.create_pass.set_tooltip(PASSWORD_FORMAT_HINT)
        self.create_pass.set_echo_mode(QLineEdit.EchoMode.Password)
        self.confirm_pass = InputEdit("Confirm new password:")
        self.confirm_pass.set_tooltip(MATCHING_PASSWORD_HINT)
        self.confirm_pass.set_echo_mode(QLineEdit.EchoMode.Password)

        self.fields = [
            self.firstname, self.lastname,
            self.dob, self.phonenum,
            self.email, self.address,
            self.create_pass,
            self.confirm_pass
        ]

        # Add fields to layout.
        self.layout = QVBoxLayout()
        self.add_row(self.firstname, self.lastname)
        self.add_row(self.dob, self.phonenum)
        self.add_row(self.email)
        self.add_row(self.address)
        self.add_row(self.create_pass, self.confirm_pass)

        self.setLayout(self.layout)

    def add_row(self, *fields):
        """Add arbitrary amount of fields to row."""
        row = QHBoxLayout()
        for field in fields:
            row.addWidget(field)
        # Add row to layout.
        self.layout.addLayout(row)

    def get_credentials(self):
        """Return dict of valid user data or None."""
        values = {
            "firstname": self.firstname.text().title(),
            "lastname":  self.lastname.text().title(),
            "dob": self.dob.date(),
            "phonenum": self.phonenum.text(),
            "email": self.email.text().lower(),
            "address": self.address.text(),
            "create_pass": self.create_pass.text(),
            "confirm_pass": self.confirm_pass.text()
        }

        is_valid = self._check_validation(values)

        if is_valid:
            return values
        return None

    def _check_validation(self, values) -> bool:
        """Validate credentials and show validation hints."""
        self._reset_validation_hints()

        # Return a mapping of field instances to their format validity.
        validation_checks: list[bool] = [
            values["firstname"] != "",
            values["lastname"] != "",
            validate_dob(values["dob"]),
            validate_phonenum(values["phonenum"]),
            validate_email(values["email"]),
            values["address"] != "",
            validate_password(values["create_pass"]),
            values["create_pass"] == values["confirm_pass"]
        ]


        flag = True
        # Store bool indication of whether all fields have valid formats (True).
        for field, is_valid in zip(self.fields, validation_checks):
            if not is_valid:
                field.show_error()
                flag = False

        try:
            if not is_email_unique(values["email"]):
                self.email.show_error()
                self.parent_scene.info_popup("This email address is already in use!")
                flag = False
        except sqlite3.Error:
            # If email uniqueness cannot be verified, terminate process.
            self.parent_scene.critical_popup(ErrorMessage.DATABASE_ERROR)
            flag = False
        return flag

    def _reset_validation_hints(self):
        """Remove error hinting."""
        for field in self.fields:
            field.clear_error()

    def reset_fields(self):
        """Clear text + error hinting from fields."""
        for field in self.fields:
            field.reset()