import datetime
import logging
import sqlite3

from PyQt6.QtWidgets import QLineEdit, QDialog, QTableWidgetItem, QTableWidget, \
    QHeaderView

from src.core.database import DatabaseConnection
from src.scenes import BaseScene
from src.signals import signals
from src.ui import UiCustomerDashboard
from src.utils.validation import *
from src.widgets import SystemFeedback, BookingItem

logger = logging.getLogger(__name__)
class CustomerDashboardScene(BaseScene, UiCustomerDashboard):
    """
    View controller for the Customer Dashboard.
    Inherits from base scene and pyuic6 converted UI file.
    """
    def __init__(self):
        super().__init__("customer-dashboard")
        self.setupUi(self)
        self.active_booking = None

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
        self.confirm_booking_btn.clicked.connect(self._on_make_booking)

        # VIEW BOOKED RIDES TABLE
        self.booking_table_widget.setColumnCount(4)
        self.booking_table_widget.setHorizontalHeaderLabels(["Driver Name", "Pickup", "Destination", "Status"])
        self.booking_table_widget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.booking_table_widget.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.booking_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.booking_table_widget.verticalHeader().hide()

        #VIEW BOOKED RIDES TABLE
        self.booking_table_widget.setColumnCount(5)
        self.booking_table_widget.setHorizontalHeaderLabels(["First Name", "Last Name", "Pickup", "Destination", "Status"])
        self.booking_table_widget.verticalHeader().hide()
        #self.load_data()

    # --- LOAD DATA FROM DATABASE TO TABLE
    #def load_data(self):
        #with DatabaseConnection() as conn:
            #bookings = conn.fetch_bookings(customer_id=self.user.id)

        self.booking_table_widget.setRowCount(25)



        # DRIVER APPLICATION PAGE -----
        # --- button events (switch to panel, cancel/confirm application)
        self.driver_btn.clicked.connect(
            lambda: self.switch_to(self.become_driver_page))
        self.cancel_driver_reg_btn.clicked.connect(
            lambda: self.switch_to(self.homePage))
        self.confirm_driver_reg_btn.clicked.connect(self._start_driver_application)



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

    def _start_driver_application(self):
        """Collect driver application and save to database."""
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
            self.info_popup(SystemFeedback.DATABASE_ERROR)
            logger.exception(e)
        else:
            self.info_popup("Application submitted! "
                            "Please give administration "
                            "time to review your application.")
            self.refresh_scene()


    def _on_make_booking(self):
        """Collect information and save to database.."""
        if self.active_booking:
            self.info_popup("Please cancel/finish any active booking before making a new one.")
            return

        info = {
            "pickup": self.pick_up_input.text(),
            "dropoff": self.drop_off_input.text(),
        }

        if info["dropoff"] == "" or info["pickup"] == "":
            self.info_popup("Please enter both a pickup location and destination.")
            return

        info.update({
            "customer_id": self.user.id,
             "date": datetime.date.today(),
             "time": datetime.datetime.now().strftime("%H-%M-%S"),
             "status": "waiting_for_assignment"
        })

        try:
            with DatabaseConnection() as conn:
                conn.create_booking(info)
        except sqlite3.Error:
            self.info_popup(SystemFeedback.DATABASE_ERROR)
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
        bookings = []
        try:
            with DatabaseConnection() as conn:
                bookings = conn.fetch_bookings(customer_id=self.user.id)

                for i, booking in enumerate(bookings):
                    if booking.status in ("waiting_for_assignment", "waiting_for_pickup", "in_process"):
                        self.active_booking = booking
                        break
        except sqlite3.Error:
            self.info_popup(SystemFeedback.DATABASE_ERROR)

        # Populate active bookings (Should only have one booking at a time.)
        if bookings:
            bookings.sort(key=lambda bk: (bk.date, bk.time), reverse=True)
            self.booking_table_widget.setRowCount(len(bookings))
            # Name column
            for row, booking in enumerate(bookings):
                if booking.driver_id:
                    self.booking_table_widget.setItem(
                        row, 0, QTableWidgetItem(booking.driver.fullname))
                else:
                    self.booking_table_widget.setItem(
                        row, 0, QTableWidgetItem("N/A"))
                # Pickup location column
                self.booking_table_widget.setItem(
                    row, 1, QTableWidgetItem(booking.pickup))
                # Destination column
                self.booking_table_widget.setItem(
                    row, 2, QTableWidgetItem(booking.dropoff))
                # Booking status column
                self.booking_table_widget.setItem(
                    row, 3, QTableWidgetItem(booking.get_formatted_status))


        try:
            # Clean up connections/signals if present.
            self.booking_table_widget.itemClicked.disconnect()
        except TypeError:
            pass

        self.booking_table_widget.itemClicked.connect(
            lambda item: self._show_booking_dialog(
                bookings[item.row()])
        )

    def _show_booking_dialog(self, booking):
        dialog = BookingItem(
            booking=booking,
            viewer="customer",
            parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_scene()

    def _log_out(self):
        """Return to launch screen."""
        signals.request_login.emit()
        self.user = None

    def clear_errors(self):
        for field in self.account_fields:
            field.clear_error()


    def depopulate_data(self):
        for field in self.account_fields:
            field.reset()
        self.active_booking = None

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
        self._load_bookings()
