import sqlite3
from typing import override, Dict

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QDateEdit

from database.db import DatabaseConnection
from src.app.scenes.base import BaseScene
from src.app.widgets.button import Button
from src.app.widgets.form_layout import FormLayout
from src.app.widgets.input_edit import InputEdit, ToolTip
from src.utils.validation import Validator


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
        self.dob = InputEdit("Enter date of birth:", QDateEdit)
        self.dob.setToolTip(ToolTip.AGE_REQUIREMENT)
        # Phone number field + tooltip.
        self.phonenum = InputEdit("Enter phone number:")
        self.phonenum.setToolTip(ToolTip.PHONENUM_FORMAT)
        # Email field + tooltip.
        self.email = InputEdit("Enter email address:")
        self.email.setToolTip(ToolTip.EMAIL_FORMAT)
        # Password fields + tooltips.
        self.create_pass = InputEdit("Create new password:")
        self.create_pass.setToolTip(ToolTip.PASSWORD_FORMAT)
        self.confirm_pass = InputEdit("Confirm new password:")
        self.confirm_pass.setToolTip(ToolTip.MATCHING_PASSWORD)

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
        self._reset_fields()
        self.signals.request_splash.emit()

    def _start_registration(self):
        """Start the registration process."""
        credentials = self._get_credentials()
        if not self._check_validation(credentials):
            return

        try:
            with DatabaseConnection as db:
                db.execute("""""") # Make database operation
        except sqlite3.Error as e:
            print(f"Handled database exception: {e}")
        except Exception as e:
            print(f"Handled unexpected exception: {e}")

        print("Successfully registered!")
        self._return_to_menu()

    def _get_credentials(self):
        """Return dict of field values."""
        credentials = {
            "firstname": self.firstname.value().title(),
            "lastname":  self.lastname.value().title(),
            "dob": self.dob.value(),
            "phonenum": self.phonenum.value(),
            "email": self.email.value().lower(),
            "created_pass": self.create_pass.value(),
            "confirmed_pass": self.confirm_pass.value()
        }
        return credentials

    def _check_validation(self, credentials: Dict[str, str | QDate]) -> bool:
        """Validate credentials and return errors, if applicable."""
        self._reset_validation_hints()
        flag = True
        # Validate name fields.
        if not Validator.firstname_check(credentials["firstname"]):
            self.firstname.show_error()
            flag = False
        if not Validator.lastname_check(credentials["lastname"]):
            self.lastname.show_error()
            flag = False
        # Validate date of birth.
        if not Validator.dob_check(credentials["dob"]):
            self.dob.show_error()
            flag = False
        # Validate phone number.
        if not Validator.phonenum_check(credentials["phonenum"]):
            self.phonenum.show_error()
            flag = False
        # Validate email address.
        if not Validator.email_check(credentials["email"]):
            self.email.show_error()
            flag = False
        # Validate password.
        if not Validator.password_check(credentials["created_pass"]):
            self.create_pass.show_error()
            flag = False
        # Validate matching passwords.
        if not Validator.match_passwords(
                credentials["created_pass"], credentials["confirmed_pass"]):
            self.confirm_pass.show_error()
            flag = False
        return flag

    def _reset_validation_hints(self):
        """Remove error hinting."""
        self.firstname.clear_error()
        self.lastname.clear_error()
        self.dob.clear_error()
        self.phonenum.clear_error()
        self.email.clear_error()
        self.create_pass.clear_error()
        self.confirm_pass.clear_error()

    def _reset_fields(self):
        """Remove error hinting and clear fields."""
        self.firstname.clear_value()
        self.lastname.clear_value()
        self.dob.clear_value()
        self.phonenum.clear_value()
        self.email.clear_value()
        self.create_pass.clear_value()
        self.confirm_pass.clear_value()














