import sqlite3
from typing import override

from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, \
    QLabel, QFrame

from src.core.database import DatabaseConnection
from src.widgets import SystemFeedback
from src.scenes import BaseScene
from src.signals import signals
from src.utils import validate_email, validate_password, validate_phonenum, \
    validate_dob, is_email_unique
from src.widgets import Button, InputEdit, DateEdit
from src.utils.constants import FieldHint


class RegisterScene(BaseScene):
    """Register scene class for the application."""

    def __init__(self):
        super().__init__(scene_name="register")
        self._load_ui()

    @override
    def _load_ui(self):
        """Setup UI."""

        # Form header.
        header = QLabel("Create a New Account")
        header.setObjectName("HEADER")
        header.setFixedHeight(80)

        # Custom divider.
        divider = QWidget()
        divider.setObjectName("DIVIDER")
        divider.setFixedHeight(3)

        # Name fields.
        self.firstname = InputEdit("Enter first name:")
        self.lastname = InputEdit("Enter last name:")
        # Date of birth field + tooltip.
        self.dob = DateEdit("Enter date of birth:")
        self.dob.set_tooltip(FieldHint.AGE_REQUIREMENT_HINT)
        # Phone number field + tooltip.
        self.phonenum = InputEdit("Enter phone number:")
        self.phonenum.set_tooltip(FieldHint.PHONENUM_FORMAT_HINT)
        # Email field + tooltip.
        self.email = InputEdit("Enter email address:")
        self.email.set_tooltip(FieldHint.EMAIL_FORMAT_HINT)
        # Password fields + tooltips.
        self.create_pass = InputEdit("Create new password:")
        self.create_pass.set_tooltip(FieldHint.PASSWORD_FORMAT_HINT)
        self.create_pass.set_echo_mode(QLineEdit.EchoMode.Password)
        self.confirm_pass = InputEdit("Confirm new password:")
        self.confirm_pass.set_tooltip(FieldHint.MATCHING_PASSWORD_HINT)
        self.confirm_pass.set_echo_mode(QLineEdit.EchoMode.Password)

        self.fields = [
            self.firstname, self.lastname,
            self.dob, self.phonenum,
            self.email,
            self.create_pass,
            self.confirm_pass
        ]

        self.form_layout = QVBoxLayout()
        self.form_layout.addWidget(header)
        self.form_layout.addWidget(divider)
        # Add fields to layout.
        self.add_row(self.firstname, self.lastname)
        self.add_row(self.dob, self.phonenum)
        self.add_row(self.email)
        self.add_row(self.create_pass, self.confirm_pass)

        form = QFrame()
        form.setLayout(self.form_layout)
        form.setObjectName("register-form")

        # Make user form buttons.
        back_btn = Button("Return to Sign In", self._return_to_signin)
        register_btn = Button("Sign Up", self._start_registration)

        # Buttons for filling out user form.
        btns = QHBoxLayout()
        btns.addWidget(back_btn)
        btns.addStretch()
        btns.addWidget(register_btn)

        # Add all elements to scene's layout.
        container = QVBoxLayout()
        container.addWidget(header)
        container.addWidget(divider)
        container.addWidget(form)
        container.addLayout(btns)

        # Set layout to scene.
        self.setLayout(container)

    def _return_to_signin(self):
        signals.trigger_refresh.emit()
        signals.request_login.emit()

    def _start_registration(self):
        """Start the registration process."""

        try:
            # Get credentials from fields.
            new_user = self.get_credentials()
            # If credentials not valid, terminate process.
            if new_user is None:
                return

            # Save user to db.
            with DatabaseConnection() as conn:
                conn.create_user(new_user,)
        except sqlite3.Error:
            self.info_popup(SystemFeedback.DATABASE_ERROR)
        else:
            self.info_popup("Successfully registered! Redirecting back to landing screen…")
            self._return_to_signin()

    def get_credentials(self):
        """Return dict of valid user data or None."""
        values = {
            "firstname": self.firstname.text().title(),
            "lastname": self.lastname.text().title(),
            "dob": self.dob.date(),
            "phonenum": self.phonenum.text(),
            "email": self.email.text().lower(),
            "create_pass": self.create_pass.text(),
            "confirm_pass": self.confirm_pass.text()
        }

        is_valid = self._check_validation(values)

        if is_valid:
            # Convert QDate to str.
            values["dob"] = values["dob"].toString("yyyy-MM-dd")
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
            validate_password(values["create_pass"]),
            values["create_pass"] == values["confirm_pass"]
        ]

        flag = True
        # Store bool indication of whether all fields have valid formats (True).
        for field, is_valid in zip(self.fields, validation_checks):
            if not is_valid:
                field.show_error()
                flag = False

        if not is_email_unique(values["email"]):
            self.email.show_error()
            self.info_popup("This email is already in use!")
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

    def refresh_scene(self):
        """Remove error hinting and clear fields."""
        self.reset_fields()

    def add_row(self, *fields):
        """Add arbitrary amount of fields to row."""
        row = QHBoxLayout()
        for field in fields:
            row.addWidget(field)
        # Add row to layout.
        self.form_layout.addLayout(row)














