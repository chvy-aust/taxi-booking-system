import sqlite3

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit

from ..core import DatabaseConnection
from ..scenes import BaseScene
from ..signals import signals
from ..ui import UiRegister
from ..utils.validation import *
from ..utils.constants import DB_ERROR


class RegisterScene(BaseScene, UiRegister):
    """Register scene class for the application."""
    def __init__(self):
        super().__init__("register")
        self.setupUi(self)
        self._load_ui()

        self.fields = [
            self.firstname, self.lastname,
            self.dob, self.phonenum,
            self.email,
            self.create_pass,
            self.confirm_pass,
            self.home_address,
            self.work_address
        ]
        self.addresses = []

    def _load_ui(self):
        # Register -> Login
        self.signin_link.clicked.connect(self._return_to_signin)

        # Hide characters in password fields.
        self.create_pass.set_echo_mode(QLineEdit.EchoMode.Password)
        self.confirm_pass.set_echo_mode(QLineEdit.EchoMode.Password)

        # Setup validation hinting
        self.firstname.set_error("\u26A0 Please enter a firstname.")
        self.lastname.set_error("\u26A0 Please enter a lastname.")
        self.dob.set_error("\u26A0 You must be 18 years or over to use this service.")
        self.email.set_error("\u26A0 Please enter a valid email.")
        self.phonenum.set_error("\u26A0 Please enter a valid phone number. "
                                "(Digits and spaces only)")
        self.create_pass.set_error("\u26A0 This password is not strong enough.")
        self.confirm_pass.set_error("\u26A0 These passwords do not match.")

        # Registration Step One - Basic User Creds (Email, Pass)
        self.signup_btn.clicked.connect(self._create_new_acc)
        self.signup_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        # Registration Step Two - Additional User Creds (Name, Dob, Phonenum)
        self.continue_btn.clicked.connect(self._complete_profile)
        # Registration Step Three - Optional Addresses
        self.skip_btn.clicked.connect(self._start_registration)
        self.confirm_btn.clicked.connect(self._get_started)

        self.page.setCurrentWidget(self.step_one)

    def _return_to_signin(self):
        self.page.setCurrentWidget(self.step_one)
        signals.request_login.emit()

    def _start_registration(self):
        """Save the user to the database."""
        try:
            with DatabaseConnection() as conn:
                conn.create_user(self.info,)
                if self.addresses:
                    user = conn.fetch_users(email=self.info["email"],)[0]
                    for address in self.addresses:
                        address["customer_id"] = user.id
                        conn.save_address(address,)
        except sqlite3.Error:
            self.info_popup(DB_ERROR)
        else:
            self.info_popup("Successfully registered! Redirecting back to landing screen…")
            self._return_to_signin()

    def _create_new_acc(self):
        """
        Create the user's account.
        Allow the user to move on once info is valid.
        """
        self.info = {
            "email": self.email.text().lower(),
            "create_pass": self.create_pass.text(),
            "confirm_pass": self.confirm_pass.text()
        }

        validation_checks = {
            self.email: validate_email(self.info["email"]),
            self.create_pass: validate_password(self.info["create_pass"]),
            self.confirm_pass:
                self.info["create_pass"] == self.info["confirm_pass"]
        }

        # Ensure all fields are valid + email unique.
        valid = is_fields_valid(validation_checks)
        if not is_email_unique(self.info["email"]):
            self.info_popup("This email is already in use!")
            valid = False

        if valid:
            # Normalize password key.
            self.info["password"] = self.info.pop("create_pass")
            self.page.setCurrentWidget(self.step_two)


    def _complete_profile(self):
        """
        Complete the user's profile.
        Allow the user to move on once info is valid.
        """
        self.info |= {
            "firstname": self.firstname.text().title(),
            "lastname": self.lastname.text().title(),
            "dob": self.dob.date(),
            "phonenum": self.phonenum.text()
        }

        validation_checks = {
            self.firstname: bool(self.info["firstname"]),
            self.lastname: bool(self.info["lastname"]),
            self.dob: validate_dob(self.info["dob"]),
            self.phonenum: validate_phonenum(self.info["phonenum"]),
        }

        # Ensure all fields are valid.
        valid = is_fields_valid(validation_checks)
        if valid:
            # Convert QDate to str.
           self.info["dob"] = self.info["dob"].toString("yyyy-MM-dd")
           self.page.setCurrentWidget(self.step_three)

    def _get_started(self):
        """Collect optional user addresses."""
        self.addresses.clear()
        addressing = {
            "home": self.home_address.text(),
            "work": self.work_address.text()
        }

        for name, address in addressing.items():
            if address:
                self.addresses.append({"name": name, "physical_address": address})

        if not self.addresses:
            self.info_popup("At least one address must be provided. "
                            "Otherwise, skip this process.")
            return

        self._start_registration()

    def populate_data(self):
        self.email.set_focus()

    def depopulate_data(self):
        """Remove error hinting and clear fields."""
        for field in self.fields:
            field.reset()
        self.addresses.clear()















