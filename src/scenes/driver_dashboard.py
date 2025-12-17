import sqlite3

from PyQt6.QtWidgets import QDialog

from ..core import DatabaseConnection
from ..scenes import BaseScene
from ..signals import signals
from ..ui import UiDriverDashboard
from ..utils.constants import (
    NON_ACTIVE_BOOKING_STATUS,
    BOOKING_DB_ERROR,
    USER_ACCOUNT_DB_ERROR)
from ..widgets import BookingItem, setup_table, populate_booking_table


class DriverDashboardScene(BaseScene, UiDriverDashboard):
    """
    View controller for the Driver Dashboard.
    Inherits from base scene and pyuic6 converted UI file.
    """
    def __init__(self):
        super().__init__("driver-dashboard")
        self.setupUi(self)
        self._load_ui()
        self.active_bookings, self.past_bookings = [], []

    def _load_ui(self):
        """Set up button events and table configurations."""
        # HOME BTN + LOGOUT BTN  + MENU BTN-----
        # --- button events (switch to panel)
        self.home_btn.clicked.connect(self.switch_to_home)
        self.logout_btn.clicked.connect(self._log_out)

        # VIEW ASSIGNED RIDES PAGE -----
        # --- button events (switch to panel)
        self.assigned_trips_btn.clicked.connect(self._switch_to_view_trips)
        self.back_to_home_btn.clicked.connect(self.switch_to_home)
        self.go_to_home_btn.clicked.connect(self.switch_to_home)

        # BOOKINGS TABLES -----
        # --- setup table views + columns
        booking_table_headers = ["Name", "Phone", "Pickup", "Destination", "Status"]
        setup_table(self.active_booking_table, booking_table_headers)
        setup_table(self.completed_booking_table, booking_table_headers)

    def switch_to_home(self):
        self._switch_to(self.home_page)

    def _switch_to_view_trips(self):
        self._switch_to(self.view_trip_page)

    def _switch_to(self, page):
        self.refresh_scene()
        self.driver_stackedWidget.setCurrentWidget(page)

    def _load_bookings(self):
        """
        Fetch and load driver bookings.
        Displays currently assigned booking + past bookings onto TableView.
        """
        try:
            with DatabaseConnection() as conn:
                bookings = conn.fetch_bookings(driver_id=self.user.id)
                for booking in bookings:
                    if booking.status in NON_ACTIVE_BOOKING_STATUS:
                        self.past_bookings.append(booking)
                    else:
                        # Should ideally only have one active booking.
                        self.active_bookings.append(booking)
        except sqlite3.Error:
            self.info_popup(BOOKING_DB_ERROR)

        # Add bookings to table rows.
        if self.active_bookings:
            populate_booking_table(self.active_booking_table, self.active_bookings)
        if self.past_bookings:
            populate_booking_table(self.completed_booking_table, self.past_bookings)

        try:
            # Clean up connections/signals if present.
            self.active_booking_table.itemClicked.disconnect()
            self.completed_booking_table.itemClicked.disconnect()
        except TypeError:
            pass

        # Trigger booking dialog on table row click.
        self.active_booking_table.itemClicked.connect(self._show_active_booking)
        self.completed_booking_table.itemClicked.connect(self._show_completed_booking)

    def _show_active_booking(self, item):
        booking = self.active_bookings[item.row()]
        self._show_booking_dialog(booking)

    def _show_completed_booking(self, item):
        booking = self.past_bookings[item.row()]
        self._show_booking_dialog(booking)

    def _show_booking_dialog(self, booking):
        """Display driver-based booking item (ie, show customer info.)"""
        if not booking:
            self.info_popup(BOOKING_DB_ERROR)
            return
        dialog = BookingItem(booking=booking, viewer="driver", parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_scene()

    def _log_out(self):
        """Return to launch screen."""
        signals.request_login.emit()
        self.user = None

    def depopulate_data(self):
        """Clear bookings populated."""
        self.active_booking_table.setRowCount(0)
        self.completed_booking_table.setRowCount(0)
        self.active_bookings.clear()
        self.past_bookings.clear()

    def populate_data(self):
        """Load refreshed bookings."""
        if self.user is None:
            self.info_popup(USER_ACCOUNT_DB_ERROR)
            signals.request_login.emit()
        self._load_bookings()
