import sqlite3

from PyQt6.QtWidgets import QLineEdit

from src.core.database import DatabaseConnection
from src.scenes import BaseScene
from src.signals import signals
from src.ui import UiCustomerDashboard
from src.utils.validation import *
from src.widgets import BookingListModel, SystemFeedback


class CustomerDashboardScene(BaseScene, UiCustomerDashboard):
    """
    View controller for the Customer Dashboard.
    Inherits from base scene and pyuic6 converted UI file.
    """
    def __init__(self):
        super().__init__("customer-dashboard")
        self.setupUi(self)

        # HOME BTN + LOGOUT BTN  + MENU BTN-----
        # --- button events (switch to panel)
        self.home_btn.clicked.connect(lambda: self.switch_to(self.homePage))
        self.log_out_btn.clicked.connect(self._log_out)

        # USER PROFILE SETTINGS -----
        # --- button events (switch to panel, cancel update, confirm update)
        self.account_btn.clicked.connect(lambda: self.switch_to(self.profile_page))
        self.cancel_edit_btn.clicked.connect(lambda: self.switch_to(self.homePage))
        self.update_account_btn.clicked.connect(self._update_user)

        # --- fields (user credentials)
        self.account_fields = [
            self.firstname, self.lastname, self.email,
            self.new_password, self.confirm_password
        ]
        # Hide password characters
        self.new_password.set_echo_mode(QLineEdit.EchoMode.Password)
        self.confirm_password.set_echo_mode(QLineEdit.EchoMode.Password)


        # BOOK A RIDE PAGE -----
        # --- button events (switch to panel)
        self.ride_btn.clicked.connect(lambda: self.switch_to(self.book_ride_page))

        # DRIVER APPLICATION PAGE -----
        # --- button events (switch to panel, cancel application)
        self.driver_btn.clicked.connect(
            lambda: self.switch_to(self.become_driver_page))
        self.cancel_driver_reg_btn.clicked.connect(
            lambda: self.switch_to(self.homePage))



    def switch_to(self, page):
        self.refresh_scene()
        self.customer_dash_panel.setCurrentWidget(page)

    def _update_user(self):
        """
        Compares collected credentials from user form.
        Updates user record, if new credentials are found.
        """
        # Clear error for null confirm pass field.
        self.clear_errors()
        info = {
            "firstname": self.firstname.text(),
            "lastname": self.lastname.text(),
            "phonenum": self.phonenum.text(),
            "email": self.email.text().lower(),
            "password": self.new_password.text(),
            "confirm_pass": self.confirm_password.text()
        }

        # Check for basic information.
        validation_checks = {
            # Check against null fields and formatting.
            self.firstname: bool(info["firstname"]),
            self.lastname: bool(info["lastname"]),
            self.phonenum: validate_phonenum(info["phonenum"]),
        }

        # Only check passwords if new values are provided.
        if info["password"]:
            if info["password"] == self.user.password:
                self.info_popup("Please provide a new password.")
                return
            # Check password formatting and matching.
            validation_checks |= {
                self.new_password: validate_password(info["password"]),
                self.confirm_password:
                    info["confirm_pass"] == info["password"]
            }
        else:
            info.pop("password", "confirm_pass")

        # Only check email if new value is provided.
        if info["email"] != self.user.email:
            # Check unique constraint.
            if not is_email_unique(info["email"]):
                self.info_popup("This email is already in use!")
                return
            # Check email formatting if unique.
            validation_checks |= {
                self.email: validate_email(info["email"])
            }

        # Terminate if any field is invalid.
        if not is_fields_valid(validation_checks):
            return

        # Get new credentials, drop unchanged credentials.
        new_values = self.user.compare_attr(info)
        if not new_values:
            return

        try:
            self.user.update(new_values)
        except sqlite3.Error:
            self.info_popup(SystemFeedback.DATABASE_ERROR)
        else:
            self.info_popup("Successfully updated profile!")
            self.refresh_scene()

    def _on_make_booking(self, info):
        """Collect information and save to database.."""
        try:
            info["customer_id"] = self.user.id
            with DatabaseConnection() as conn:
                conn.create_booking(info)
        except sqlite3.Error:
            self.info_popup(SystemFeedback.DATABASE_ERROR)
        else:
            self.info_popup("Successfully booked! " +
                "Please wait for a driver to be assigned to your ride…")
            self.refresh_scene()

    def _load_bookings(self):
        """Fetch and load all user bookings onto list view."""
        try:
            with DatabaseConnection() as conn:
                bookings = conn.fetch_bookings(self.user.id,)
                self.booking_list.setModel(BookingListModel(bookings))
        except sqlite3.Error:
            self.info_popup(SystemFeedback.DATABASE_ERROR)

    def _log_out(self):
        """Return to launch screen."""
        signals.request_login.emit()
        self.user = None

    def clear_errors(self):
        for field in self.account_fields:
            field.clear_error()


    def refresh_scene(self):
        self.depopulate_data()
        self.populate_data()

    def depopulate_data(self):
        for field in self.account_fields:
            field.reset()

    def populate_data(self):
        if self.user is None:
            self.info_popup("Could not access your account. Please Try Again or contact Support.")
            signals.request_login.emit()
            return
        # Preload account field text
        self.firstname.set_text(self.user.firstname)
        self.lastname.set_text(self.user.lastname)
        self.phonenum.set_text(self.user.phonenum)
        self.email.set_text(self.user.email)
        # Set account field validation hints
        self.firstname.set_error("\u26A0 Please enter a firstname.")
        self.lastname.set_error("\u26A0 Please enter a lastname.")
        self.email.set_error("\u26A0 Please enter a valid email.")
        self.phonenum.set_error("\u26A0 Invalid phone number format.")
        self.new_password.set_error("\u26A0 Password not strong enough.")
        self.confirm_password.set_error("\u26A0 These passwords do not match.")
