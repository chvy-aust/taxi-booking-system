import sqlite3

from PyQt6.QtWidgets import QTableWidgetItem

from ..core import DatabaseConnection
from ..scenes import BaseScene
from ..signals import signals
from ..ui import UiAdminDashboard
from ..utils.constants import USER_ACCOUNT_DB_ERROR, USER_DB_ERROR, \
    BOOKING_DB_ERROR, DB_ERROR
from ..widgets import BookingItem, setup_table, populate_booking_table


class AdminDashboardScene(BaseScene, UiAdminDashboard):
    """
    View controller for the Admin Dashboard.
    Inherits from base scene and pyuic6 converted UI file.
    """
    def __init__(self):
        super().__init__("admin-dashboard")
        self.setupUi(self)
        self._load_ui()
        self.pending_bookings, self.assigned_bookings = [], []
        self.tables = [
            self.pending_table, self.assigned_table,
            self.customer_table, self.driver_table]


    def _load_ui(self):
        """Set up button events and table configurations."""
        # HOME BTN + LOGOUT BTN  + MENU BTN-----
        # --- button events (switch to panel)
        self.home_btn.clicked.connect(self.switch_to_home)
        self.menu_btn.clicked.connect(
            lambda: self.info_popup("This feature is coming soon!"))
        self.logout_btn.clicked.connect(self._log_out)

        # ASSIGN DRIVER PAGE -----
        # --- button events (switch to panel)
        self.assign_drivers_btn.clicked.connect(self._switch_to_assign_drivers)
        self.admin_back_home_btn.clicked.connect(self.switch_to_home)

        # BOOKINGS TABLE ----
        # --- setup table views + columns
        booking_table_headers = ["Customer", "Phone", "Pickup", "Destination", "Status"]
        setup_table(self.pending_table, booking_table_headers)
        setup_table(self.assigned_table, booking_table_headers)

        # VIEW USERS PAGE -----
        # --- button events (switch to panel)
        self.view_users_btn.clicked.connect(self._switch_to_view_users)
        self.back_to_home_btn.clicked.connect(self.switch_to_home)

        # USERS TABLE -----
        # --- setup table views + columns
        user_table_headers = ["User ID", "Name", "Email", "Phone", "Role"]
        setup_table(self.customer_table, user_table_headers)
        setup_table(self.driver_table, user_table_headers)


    def switch_to_home(self):
        self._switch_to(self.home_page)

    def _switch_to_view_users(self):
        self._switch_to(self.view_users_page)

    def _switch_to_assign_drivers(self):
        self._switch_to(self.assign_drivers_page)

    def _switch_to(self, page):
        self.refresh_scene()
        self.admin_stackedWidget.setCurrentWidget(page)

    def _load_users(self):
        """Fetch and load customer + driver users onto TableView."""
        try:
            with DatabaseConnection() as conn:
                users = conn.fetch_users(role=("customer", "driver"))
        except sqlite3.Error:
            self.info_popup(USER_DB_ERROR)

        customer_table_row, driver_table_row = 0, 0

        for user in users:
            if user.role == "customer":
                table = self.customer_table
                current_row = customer_table_row
                customer_table_row += 1
            else:
                table = self.driver_table
                current_row = driver_table_row
                driver_table_row += 1

            table.insertRow(current_row)
            table.setItem(current_row, 0, QTableWidgetItem(str(user.id)))
            table.setItem(current_row, 1, QTableWidgetItem(user.fullname))
            table.setItem(current_row, 2, QTableWidgetItem(user.email))
            table.setItem(current_row, 3, QTableWidgetItem(user.phonenum))
            table.setItem(current_row, 4, QTableWidgetItem(user.role))

    def _load_bookings(self):
        """
        Fetch and load admin bookings.
        Displays bookings waiting for assignment + assigned bookings onto TableView.
        """
        try:
            with DatabaseConnection() as conn:
                bookings = conn.fetch_bookings()
                for booking in bookings:
                    if booking.status == 'waiting_for_assignment':
                        self.pending_bookings.append(booking)
                    else:
                        self.assigned_bookings.append(booking)
        except sqlite3.Error:
            self.info_popup(BOOKING_DB_ERROR)


        if self.pending_bookings:
            populate_booking_table(self.pending_table, self.pending_bookings)
        if self.assigned_bookings:
            populate_booking_table(self.assigned_table, self.assigned_bookings)

        try:
            # Clean up connections/signals if present.
            self.pending_table.itemClicked.disconnect()
            self.assigned_table.itemClicked.disconnect()
        except TypeError:
            pass

        # Show dialog when item is clicked.
        self.assigned_table.itemClicked.connect(self._show_assigned_bookings)
        self.pending_table.itemClicked.connect(self._show_pending_bookings)

    def _show_pending_bookings(self, item):
        booking = self.pending_bookings[item.row()]
        self._show_booking_dialog(booking)

    def _show_assigned_bookings(self, item):
        booking = self.assigned_bookings[item.row()]
        self._show_booking_dialog(booking)

    def _show_booking_dialog(self, booking):
        """Display driver-based booking item (ie, show customer and driver info.)"""
        try:
            dialog = BookingItem(booking=booking, viewer="admin", parent=self)
            dialog.exec()
        except sqlite3.Error:
            self.info_popup(DB_ERROR)
        self.refresh_scene()

    def _log_out(self):
        """Return to launch screen."""
        signals.request_login.emit()
        self.user = None

    def depopulate_data(self):
        """Clear tables and fetched bookings."""
        for table in self.tables:
            table.setRowCount(0)
        self.pending_bookings.clear()
        self.assigned_bookings.clear()

    def populate_data(self):
        """Load refreshed user records and bookings."""
        if self.user is None:
            self.info_popup(USER_ACCOUNT_DB_ERROR)
            signals.request_login.emit()
        self._load_users()
        self._load_bookings()
