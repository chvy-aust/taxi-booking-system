import sqlite3
from typing import override

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout,  QLineEdit
from PyQt6 import uic


from database.db import DatabaseConnection
from src.app.scenes import BaseScene
from src.app.widgets import Button, FormLayout, InputEdit, DateEdit
from src.utils.constants import FieldHint, ErrorMessage
from src.utils.validation import validate_phonenum, validate_dob, \
    validate_email, validate_password, is_email_unique


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

        # Name fields.
        self.firstname = InputEdit("Enter first name:")
        self.lastname = InputEdit("Enter last name:")
        # Date of birth field + tooltip.
        self.dob = DateEdit("Enter date of birth:")
        self.dob.set_tooltip(FieldHint.AGE_REQUIREMENT)
        # Phone number field + tooltip.
        self.phonenum = InputEdit("Enter phone number:")
        self.phonenum.set_tooltip(FieldHint.PHONENUM_FORMAT)
        # Email field + tooltip.
        self.email = InputEdit("Enter email address:")
        self.email.set_tooltip(FieldHint.EMAIL_FORMAT)
        self.address = InputEdit("Enter home address:")
        # Password fields + tooltips.
        self.create_pass = InputEdit("Create new password:")
        self.create_pass.set_tooltip(FieldHint.PASSWORD_FORMAT)
        self.create_pass.set_echo_mode(QLineEdit.EchoMode.Password)
        self.confirm_pass = InputEdit("Confirm new password:")
        self.confirm_pass.set_tooltip(FieldHint.MATCHING_PASSWORD)
        self.confirm_pass.set_echo_mode(QLineEdit.EchoMode.Password)

        self.fields = [
            self.firstname, self.lastname,
            self.dob, self.phonenum,
            self.email, self.address,
            self.create_pass,
            self.confirm_pass
        ]

        # Add fields to form layout.
        form_layout = FormLayout()
        form_layout.add_row(self.firstname, self.lastname)
        form_layout.add_row(self.dob, self.phonenum)
        form_layout.add_row(self.email)
        form_layout.add_row(self.address)
        form_layout.add_row(self.create_pass, self.confirm_pass)

        # Make form with layout.
        form = QWidget()
        form.setObjectName("register_form")
        form.setLayout(form_layout)

        # Make buttons.
        back_btn = Button("Return to Main Menu", self._return_to_menu)
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

    def _return_to_menu(self):
        self.signals.trigger_refresh.emit()
        self.signals.request_splash.emit()

    def _start_registration(self):
        """Start the registration process."""
        # Get credentials from fields.
        values = self._get_credentials()
        # If credentials not valid, terminate process.
        if not self._check_validation(values):
            return

        try:
            # Save user to database.
            with DatabaseConnection() as conn:
                conn.create_user(
                    values["firstname"],
                    values["lastname"],
                    # Convert QDate to str.
                    values["dob"].toString("yyyy-MM-dd"),
                    values["phonenum"],
                    values["email"],
                    values["address"],
                    values["create_pass"],)
        except sqlite3.Error:
            self.critical_popup(ErrorMessage.DATABASE_ERROR)
        else:
            self.info_popup("Successfully registered! Redirecting back to landing screen…")
            self._return_to_menu()

    def _get_credentials(self):
        """Return dict of field values."""
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
        return values

    def _check_validation(self, values) -> bool:
        """Validate credentials and show validation hints."""
        self._reset_validation_hints()

        # Return a mapping of field instances to their format validity.
        validation_checks = [
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
                self.info_popup("This email address is already in use!")
                flag = False
        except sqlite3.Error:
            # If email uniqueness cannot be verified, terminate process.
            self.critical_popup(ErrorMessage.DATABASE_ERROR)
            flag = False
        return flag

    def _reset_validation_hints(self):
        """Remove error hinting."""
        for field in self.fields:
            field.clear_error()

    @override
    def refresh_scene(self):
        """Remove error hinting and clear fields."""
        for field in self.fields:
            field.reset()












