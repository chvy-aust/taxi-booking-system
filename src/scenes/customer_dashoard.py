import datetime
import logging
import sqlite3

from PyQt6.QtWidgets import QLineEdit, QDialog, QTableWidgetItem

from ..core import DatabaseConnection
from ..scenes import BaseScene
from ..signals import signals
from ..ui import UiCustomerDashboard
from ..utils import BOOKING_DB_ERROR
from ..utils.constants import USER_ACCOUNT_DB_ERROR, ACTIVE_BOOKING_STATUS, DB_ERROR
from ..utils.validation import *
from ..widgets import BookingItem, setup_table

logger = logging.getLogger(__name__)
class CustomerDashboardScene(BaseScene, UiCustomerDashboard):
    """
    View controller for the Customer Dashboard.
    Inherits from base scene and pyuic6 converted UI file.
    """
    def __init__(self):
        super().__init__("customer-dashboard")
        self.setupUi(self)
        self._load_ui()
        self.bookings, self.active_booking = [], None

        self.account_fields = [
            self.firstname, self.lastname, self.email,
            self.new_password, self.confirm_password
        ]

    def _load_ui(self):
        """
        Setup button events and table configurations.
        Hide characters in password fields.
        """
        # HOME BTN + LOGOUT BTN  + MENU BTN-----
        # --- button events (switch to panel)
        self.home_btn.clicked.connect(self.switch_to_home)
        self.menu_btn.clicked.connect(
            lambda: self.info_popup("This feature is coming soon!"))
        self.log_out_btn.clicked.connect(self._log_out)

        # USER PROFILE SETTINGS -----
        # --- button events (switch to panel, cancel update, confirm update)
        self.account_btn.clicked.connect(self._switch_to_profile_page)
        self.cancel_edit_btn.clicked.connect(self.switch_to_home)
        self.update_account_btn.clicked.connect(self._update_user)

        # Hide password characters
        self.new_password.set_echo_mode(QLineEdit.EchoMode.Password)
        self.confirm_password.set_echo_mode(QLineEdit.EchoMode.Password)

        # BOOK A RIDE PAGE -----
        # --- button events (switch to panel)
        self.ride_btn.clicked.connect(self._switch_to_book_ride)
        self.confirm_booking_btn.clicked.connect(self._on_make_booking)

        # --- setup table views + columns
        booking_table_headers = ["Driver Name", "Pickup", "Destination", "Status"]
        setup_table(self.booking_table_widget, booking_table_headers)

        # DRIVER APPLICATION PAGE -----
        # --- button events (switch to panel, cancel/confirm application)
        self.driver_btn.clicked.connect(self._switch_to_become_driver)
        self.cancel_driver_reg_btn.clicked.connect(self.switch_to_home)
        self.confirm_driver_reg_btn.clicked.connect(self._start_driver_application)

    def switch_to_home(self):
        self._switch_to(self.home_page)

    def _switch_to_profile_page(self):
        self._switch_to(self.profile_page)

    def _switch_to_book_ride(self):
        self._switch_to(self.book_ride_page)

    def _switch_to_become_driver(self):
        self._switch_to(self.become_driver_page)

    def _switch_to(self, page):
        self.refresh_scene()
        self.customer_dash_panel.setCurrentWidget(page)

    def _update_user(self):
        """
        Compares collected credentials from user form.
        Updates user record, if new credentials are found.
        """
        # Clear error for null confirm pass field.
        info = {
            "firstname": self.firstname.text(),
            "lastname": self.lastname.text(),
            "phonenum": self.phonenum.text(),
            "email": self.email.text().lower(),
            "password": self.new_password.text(),
            "confirm_pass": self.confirm_password.text()
        }

        # Validate user input.
        if not self._validate_user_update(info):
            return

        # Get new credentials, drop unchanged credentials.
        new_values = self.user.compare_attr(info)
        if not new_values:
            return

        try:
            self.user.update(new_values)
        except sqlite3.Error:
            self.info_popup(DB_ERROR)
        else:
            self.info_popup("Successfully updated profile!")
            self.refresh_scene()

    def _validate_user_update(self, info: dict[str, str]) -> bool:
        """Return True if new credentials are all valid, else False"""
        validation_checks = {
            # Check against null fields and formatting.
            self.firstname: bool(info["firstname"]),
            self.lastname: bool(info["lastname"]),
            self.phonenum: validate_phonenum(info["phonenum"]),
        }

        # Only check passwords if new values are provided.
        if info["password"] or info["confirm_pass"]:
            # Check password formatting and matching.
            validation_checks.update({
                self.new_password: validate_password(info["password"]),
                self.confirm_password:
                    info["confirm_pass"] == info["password"]
            })
        else:
            info.pop("password", "confirm_pass")

        # Only check email if new value is provided.
        if info["email"] != self.user.email:
            # Check unique constraint.
            if not is_email_unique(info["email"]):
                self.info_popup("This email is already in use!")
                return False
            # Check email formatting if unique.
            validation_checks.update({
                self.email: validate_email(info["email"])
            })

        if not is_fields_valid(validation_checks):
            return False
        return True

    def _start_driver_application(self):
        """
        Collect driver application and save to database.
        Automatically refresh scene on success.
        """
        info = {
            "user_id": self.user.id,
            "car_make": self.car_make.text(),
            "car_model": self.car_model.text(),
            "car_colour": self.car_colour.text(),
            "man_year": self.manufacture_year.text(),
            "plate_num": self.license_plate_reg.text(),
            "status": "pending",
            "submitted_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            with DatabaseConnection() as conn:
                conn.create_driver_application(info)
        except sqlite3.Error as e:
            self.info_popup(DB_ERROR)
        else:
            self.info_popup("Application submitted! "
                            "Please give administration "
                            "time to review your application.")
            self.refresh_scene()


    def _on_make_booking(self):
        """
        Collect booking information and create new db record.
        Automatically refresh scene on success.
        """
        if self.active_booking:
            self.info_popup("Please cancel/finish any active booking before making a new one.")
            return

        pickup = self.pick_up_input.text()
        dropoff = self.drop_off_input.text()

        if pickup == "" or dropoff == "":
            self.info_popup("Please enter both a pickup location and destination.")
            return

        info = {
            "customer_id": self.user.id,
            "dropoff": dropoff,
            "pickup": pickup,
            "date": datetime.date.today(),
            "time": datetime.datetime.now().strftime("%H-%M-%S"),
            "status": "waiting_for_assignment"
        }

        try:
            with DatabaseConnection() as conn:
                conn.create_booking(info)
        except sqlite3.Error:
            self.info_popup(DB_ERROR)
        else:
            self.info_popup("Successfully booked! "
                            "Please wait for a driver "
                            "to be assigned to your ride…")
            self.refresh_scene()


    def _load_bookings(self):
        """
        Fetch and load driver bookings.
        Displays currently assigned booking + past bookings onto TableView.
        """
        try:
            with DatabaseConnection() as conn:
                self.bookings = conn.fetch_bookings(customer_id=self.user.id)
                for i, booking in enumerate(self.bookings):
                    if booking.status in ACTIVE_BOOKING_STATUS:
                        self.active_booking = booking
                        break
        except sqlite3.Error:
            self.info_popup(BOOKING_DB_ERROR)

        # Populate active bookings (Should only have one booking at a time.)
        if self.bookings:
            self.bookings.sort(
                key=lambda bk: (bk.date, bk.time),
                reverse=True
            )
            self.booking_table_widget.setRowCount(len(self.bookings))
            for row, booking in enumerate(self.bookings):
                value = "N/A"
                if booking.driver_id:
                    value = booking.driver.fullname
                self.booking_table_widget.setItem(row, 0, QTableWidgetItem(value))
                self.booking_table_widget.setItem(row, 1, QTableWidgetItem(booking.pickup))
                self.booking_table_widget.setItem(row, 2, QTableWidgetItem(booking.dropoff))
                self.booking_table_widget.setItem(row, 3, QTableWidgetItem(booking.formatted_status))


        try:
            # Clean up connections/signals if present.
            self.booking_table_widget.itemClicked.disconnect()
        except TypeError:
            pass

        self.booking_table_widget.itemClicked.connect(self._show_booking_dialog)

    def _show_booking_dialog(self, item):
        """Display customer-based booking item (ie, show driver info.)"""
        booking = self.bookings[item.row()]
        dialog = BookingItem(booking=booking, viewer="customer", parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_scene()

    def _log_out(self):
        """Return to launch screen."""
        signals.request_login.emit()
        self.user = None

    def depopulate_data(self):
        """Reset user account fields and bookings."""
        for field in self.account_fields:
            field.reset()
        self.active_booking = None
        self.bookings.clear()

    def populate_data(self):
        """Load user account data and booking records."""
        if self.user is None:
            self.info_popup(USER_ACCOUNT_DB_ERROR)
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
        self._load_bookings()
