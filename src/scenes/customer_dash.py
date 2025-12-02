import sqlite3

from PyQt6.QtWidgets import QVBoxLayout, QLabel, QListView, \
    QHBoxLayout, QWidget, QStackedWidget

from src.signals import signals
from src.core.database import DatabaseConnection
from src.widgets import SystemFeedback
from src.scenes import BaseScene
from src.widgets import BookingListModel, Button
from src.forms import BookingForm


class CustomerDashboardScene(BaseScene):
    def __init__(self):
        super().__init__("customer-dash")
        self._load_ui()

    def _load_ui(self):
        self.greeting = QLabel()
        self.greeting.setObjectName("dash-greeting")

        self.layout = QHBoxLayout()
        self._setup_side_panel()
        self._setup_center_panel()

        self.container = QVBoxLayout()
        self.container.addWidget(self.greeting)
        self.container.addLayout(self.layout)
        self.setLayout(self.container)

    def _setup_center_panel(self):
        """
        Configure the dashboard's center (main) panel.
        Features:
            - Account Profile Settings : Change user attributes.
            - Booking Management : Make bookings and view booking history.
        """
        self.center_panel = QStackedWidget()

        # USER ACCOUNT PROFILE
        profile_layout = QVBoxLayout()
        self.user_form = QWidget()
        update_user_btn = Button("Update", self._update_user)
        profile_layout.addWidget(self.user_form)
        profile_layout.addWidget(update_user_btn)

        self.account_panel = QWidget()
        self.account_panel.setLayout(profile_layout)
        self.center_panel.addWidget(self.account_panel)

        # BOOKING MANAGEMENT PROFILE
        booking_layout = QHBoxLayout()
        # View bookings
        booking_list_model = BookingListModel()
        self.booking_list = QListView()
        self.booking_list.setModel(booking_list_model)
        # Make a booking
        self.booking_form = BookingForm()
        self.booking_form.make_booking.connect(self._on_make_booking)
        booking_layout.addWidget(self.booking_list)
        booking_layout.addWidget(self.booking_form)

        self.booking_panel = QWidget()
        self.booking_panel.setLayout(booking_layout)
        self.center_panel.addWidget(self.booking_panel)
        # Load booking panel on initialization.
        self._load_panel(self.booking_panel)
        self.layout.addWidget(self.center_panel)

    def _setup_side_panel(self):
        """
        Configure the dashboard's side panel.
        Handles switching center panel widgets and logging out.
        """
        self.side_panel = QVBoxLayout()

        # Side panel buttons.
        view_profile_btn = Button("Account", lambda: self._load_panel(self.account_panel))
        view_bookings_btn = Button("Bookings", lambda: self._load_panel(self.booking_panel))
        self.logout_btn = Button("Log out", self._log_out)
        # Add buttons to panel
        self.side_panel.addWidget(view_profile_btn)
        self.side_panel.addWidget(view_bookings_btn)
        self.side_panel.addStretch()
        self.side_panel.addWidget(self.logout_btn)

        self.layout.addLayout(self.side_panel)


    def _update_user(self):
        """
        Compares collected credentials from user form.
        Updates user record, if new credentials are found.
        """
        # Get valid credentials from user form.
        valid_values = []
        if not valid_values:
            return

        # Get new credentials, drop unchanged credentials.
        new_values = self.user.compare_attr(valid_values)
        if not new_values:
            return

        try:
            self.user.update(new_values)
        except sqlite3.Error:
            self.info_popup(SystemFeedback.DATABASE_ERROR)
        else:
            self.info_popup("Successfully updated profile!")
            signals.trigger_refresh.emit()

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

    def _log_out(self):
        self.user = None
        signals.request_login.emit()

    def _load_panel(self, panel):
        self.center_panel.setCurrentWidget(panel)

    def refresh_scene(self):
        self._depopulate_date()
        self.populate_data()

    def populate_data(self):
        if self.user is None:
            self.info_popup("Could not access your account. Please Try Again or contact Support.")
            signals.request_login.emit()
            return

        self.greeting.setText(f"Welcome, {self.user.firstname} {self.user.lastname}!")
        self._load_bookings()

    def _load_bookings(self):
        """Fetch and load all user bookings onto list view."""
        try:
            with DatabaseConnection() as conn:
                bookings = conn.fetch_bookings(self.user.id,)
                self.booking_list.setModel(BookingListModel(bookings))
        except sqlite3.Error:
            self.info_popup(SystemFeedback.DATABASE_ERROR)


    def _depopulate_date(self):
        self.greeting.setText(None)