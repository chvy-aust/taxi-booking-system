import re
from typing import override

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QDateEdit, QLabel, QHBoxLayout

from datetime import date

from src.app.scenes.base import BaseScene
from src.app.widgets.button import Button
from src.app.widgets.form_layout import FormLayout
from src.app.widgets.input_edit import InputEdit

PHONENUM = re.compile(r"(^\+?\d{1,3}[-\s]?)?(\(\d{1,3}\)|\d{1,3})[-\s]?\d{1,3}[-\s]?\d{1,4}$")
EMAIL = re.compile(r"^[\w\-.]+@([\w-]+\.)+[\w-]{2,4}$")
PASSWORD = re.compile(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}")

AGE_REQUIREMENT_HINT = "You must be 18+ to use this service."
PHONENUM_FORMAT_HINT = ("May contain optional country code. Must have area and local code.\n"
                        "Examples of valid formats:\n"
                        "- +1 (123) 456 7890 | +1-(123)-456-7890\n"
                        "- 1 123 456 7890 | 1-123-456-7890\n"
                        "- 123 456 7890 | 123-456-7890\n")

EMAIL_FORMAT_HINT = "Must contain '@' and '.'"
PASSWORD_FORMAT_HINT = "Password must contain 1 Uppercase letter, 1 lowercase letter and 1 number."
MATCHING_PASSWORD_HINT = "These passwords do not match!"

class RegisterScene(BaseScene):
    """Register scene class for the application."""
    def __init__(self, signals):
        super().__init__(
            scene_name="register",
            signals=signals)
        self.signals = signals
        self._load_ui()

    @override
    def _load_ui(self):
        """Setup UI."""
        # Register scene header label.
        header = QLabel("Create a new Account")
        header.setObjectName("HEADER")
        header.setFixedHeight(80)

        # Custom divider.
        divider = QWidget()
        divider.setObjectName("DIVIDER")
        divider.setFixedHeight(3)

        # Make credential fields.
        self.firstname = InputEdit("Enter first name:")
        self.lastname = InputEdit("Enter last name:")
        self.dob = InputEdit("Enter date of birth:", QDateEdit, tooltip=AGE_REQUIREMENT_HINT)
        self.phonenum = InputEdit("Enter phone number:", tooltip=PHONENUM_FORMAT_HINT)
        self.email = InputEdit("Enter email address:", tooltip=EMAIL_FORMAT_HINT)
        self.create_pass = InputEdit("Create new password:", tooltip=PASSWORD_FORMAT_HINT)
        self.confirm_pass = InputEdit("Confirm new password:", tooltip=MATCHING_PASSWORD_HINT)

        self.fields = [self.firstname, self.lastname, self.dob, self.phonenum,
                            self.email, self.create_pass, self.confirm_pass]

        # Add fields to form layout.
        form_layout = FormLayout()
        form_layout.add_row(self.firstname, self.lastname)
        form_layout.add_row(self.dob, self.phonenum)
        form_layout.add_row(self.email)
        form_layout.add_row(self.create_pass, self.confirm_pass)

        # Make form with layout.
        form = QWidget()
        form.setObjectName("register_form")
        form.setLayout(form_layout)

        # Make buttons.
        back_btn = Button("Return to Main Menu", self.signals.request_splash)
        self.register_btn = Button("Register", self._start_registration)

        # Add buttons to container.
        btns = QHBoxLayout()
        btns.addWidget(back_btn)
        btns.addStretch()
        btns.addWidget(self.register_btn)

        # Add all elements to scene's layout.
        container = QVBoxLayout()
        container.addWidget(header)
        container.addWidget(divider)
        container.addWidget(form)
        container.addLayout(btns)

        # Set layout to scene.
        self.setLayout(container)

    def _start_registration(self):
        """Start the registration process."""
        credentials = self._get_credentials()
        if self._check_validation():
            return
        print("VALID!")

    def _get_credentials(self):
        credentials = {
            self.firstname: self.firstname.value().title(),
            self.lastname:  self.lastname.value().title(),
            self.dob: self.dob.value(),
            self.phonenum: self.phonenum.value(),
            self.email: self.email.value(),
            self.create_pass: self.create_pass.value()
        }
        return credentials

    def display(self, e):
        print(e)

    def _check_validation(self):
        for field in self.fields:
            field.clear_error()

        invalid_fields = []
        for field in self.fields:
            if field.value() == "":
                field.show_error()
                invalid_fields.append(field)

        if not self.validate_age(self.dob.value()):
            self.dob.show_error()
            invalid_fields.append(self.dob)

        if not re.match(PHONENUM, self.phonenum.value()):
            self.phonenum.show_error()
            invalid_fields.append(self.phonenum)

        if not re.match(EMAIL, self.email.value()):
            self.email.show_error()
            invalid_fields.append(self.email)

        if not re.match(PASSWORD, self.create_pass.value()):
            self.create_pass.show_error()
            invalid_fields.append(self.create_pass)

        if self.create_pass.value() != self.confirm_pass.value():
            self.confirm_pass.show_error()
            invalid_fields.append(self.confirm_pass)

        return invalid_fields


    def validate_age(self, dob):
        today = date.today()
        age = today.year - dob.year()
        if [today.month, today.day] > [dob.month(), dob.year()]:
            age -= 1
        return age >= 18











