import sqlite3
from typing import Any

from PyQt6.QtWidgets import QVBoxLayout, QLabel, QListView, \
    QHBoxLayout, QWidget, QStackedWidget

from database.db import DatabaseConnection
from src.widgets import BookingForm, BookingListModel, Button
from src.scenes import BaseScene
from src.models.booking import Booking
from src.dialogs import SystemFeedback


class CustomerDashboardScene(BaseScene):
    def __init__(self, signal):
        super().__init__("dashboard", signals=signal)
        self._load_ui()


    def _load_ui(self):
        # Buttons
        self.greeting = QLabel()

        self.booking_form = BookingForm()
        self.booking_form.start_booking.connect(self._handle_booking)
        self.booking_list = QListView()
        self.booking_list_model = BookingListModel()
        self.booking_list.setModel(self.booking_list_model)

        # Center panel
        booking_panel_layout = QHBoxLayout()
        booking_panel_layout.addWidget(self.booking_list)
        booking_panel_layout.addWidget(self.booking_form)

        booking_panel = QWidget()
        booking_panel.setLayout(booking_panel_layout)

        c_panel = QStackedWidget()
        c_panel.addWidget(booking_panel)


        self.logout_btn = Button("Log out", self._log_out)

        self.container = QVBoxLayout()
        self.container.addWidget(self.greeting)
        self.container.addWidget(c_panel)
        self.container.addWidget(self.logout_btn)
        self.setLayout(self.container)

    def _log_out(self):
        self.user = None
        self.signals.request_splash.emit()

    def _handle_booking(self, info):
        try:
            with DatabaseConnection() as conn:
                conn.create_booking(self.user.id, info)
        except sqlite3.Error:
            self.critical_popup(SystemFeedback.DATABASE_ERROR)
        else:
            self.info_popup(
                    "Successfully booked! " 
                    "Please wait a short moment for driver assignment…")

        self.refresh_scene()

    def _load_bookings(self):
        try:
            with DatabaseConnection() as conn:
                results = conn.fetch_bookings(self.user.id,)
        except sqlite3.Error:
            self.critical_popup(SystemFeedback.DATABASE_ERROR)
        else:
            bookings = [Booking(row) for row in results]
            self.booking_list.setModel(BookingListModel(bookings))




    def _update_user(self, new_attr: dict[str, Any]):
        """
        Return and set user with updated attributes.
        Accepts a dictionary of str attributes to their new values.
        """
        try:
            self.user.update(new_attr)
        except sqlite3.Error:
            self.critical_popup(SystemFeedback.DATABASE_ERROR)
        else:
            self.info_popup("Successfully updated profile!")
            self.signals.trigger_refresh.emit()

    def refresh_scene(self):
        self.populate_data()


    def populate_data(self):
        if self.user is None:
            self.critical_popup("Could not access your account. Please Try Again or contact Support.")
            self._depopulate_date()
            self.signals.request_splash.emit()
            return

        # Fields to populate here:
        self.greeting.setText(f"Welcome, {self.user.firstname} {self.user.lastname}!")
        self._load_bookings()


    def _depopulate_date(self):
        self.greeting.setText(None)