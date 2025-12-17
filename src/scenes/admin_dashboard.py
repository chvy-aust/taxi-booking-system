from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView, QDialog, QTableWidget

from src.widgets import SystemFeedback, populate_table, BookingItem, setup_table
from src.core.database import DatabaseConnection
from src.signals import signals
from src.scenes import BaseScene
from src.ui import UiAdminDashboard
import sqlite3


class AdminDashboardScene(BaseScene, UiAdminDashboard):
    """
    View controller for the Admin Dashboard.
    Inherits from base scene and pyuic6 converted UI file.
    """
    def __init__(self):
        super().__init__("admin-dashboard")
        self.setupUi(self)
        self._load_ui()

        # HOME BTN + LOGOUT BTN  + MENU BTN-----
        # --- button events (switch to panel)
        self.admin_home_bn.clicked.connect(lambda: self.switch_to(self.admin_home_page))
        self.admin_logout_btn.clicked.connect(self._log_out)

        # ASSIGN DRIVER PAGE -----
        # --- button events (switch to panel)
        self.assign_drivers_btn.clicked.connect(lambda: self.switch_to(self.assign_drivers_page))
        self.back_to_home_btn.clicked.connect(lambda: self.switch_to(self.admin_home_page))

        # VIEW USERS PAGE -----
        # --- button events (switch to panel)
        self.view_users_btn.clicked.connect(lambda: self.switch_to(self.view_users_page))
        self.back_to_home_btn.clicked.connect(lambda: self.switch_to(self.admin_home_page))

    def _load_ui(self):
        # setup user tables
        USER_TABLE_HEADERS = ["User ID", "Name", "Email", "Phone", "Role"]
        setup_table(self.customer_table_widget, USER_TABLE_HEADERS)
        setup_table(self.driver_table_widget, USER_TABLE_HEADERS)

        # setup booking tables
        BOOKING_TABLE_HEADERS = ["Customer", "Phone", "Pickup", "Destination","Status"]
        setup_table(self.pending_table_widget, BOOKING_TABLE_HEADERS)
        setup_table(self.assigned_table_widget, BOOKING_TABLE_HEADERS)

        # setup button events


    def _load_users(self):
        try:
            with DatabaseConnection() as conn:
                users = conn.fetch_users(role=("customer", "driver"))
        except sqlite3.Error:
            self.info_popup(SystemFeedback.DATABASE_ERROR)

        customer_table_row, driver_table_row = 0, 0

        for user in users:
            if user.role == "customer":
                table = self.customer_table_widget
                current_row = customer_table_row
                customer_table_row += 1

            elif user.role == "driver":
                table = self.driver_table_widget
                current_row = driver_table_row
                driver_table_row += 1
            else:
                continue

            table.insertRow(current_row)
            table.setItem(current_row, 0, QTableWidgetItem(str(user.id)))
            table.setItem(current_row, 1, QTableWidgetItem(user.fullname))
            table.setItem(current_row, 2, QTableWidgetItem(user.email))
            table.setItem(current_row, 3, QTableWidgetItem(user.phonenum))
            table.setItem(current_row, 4, QTableWidgetItem(user.role))

    def _load_bookings(self):
        """
        Fetch and load driver bookings.
        Displays currently assigned booking + past bookings onto TableView.
        """
        pending_booking_items, assigned_booking_items = [], []
        try:
            with DatabaseConnection() as conn:
                bookings = conn.fetch_bookings()
                for booking in bookings:
                    if booking.status == 'waiting_for_assignment':
                        pending_booking_items.append(booking)
                    else:
                        assigned_booking_items.append(booking)
        except sqlite3.Error:
            self.info_popup(SystemFeedback.DATABASE_ERROR)

        if pending_booking_items:
            self.pending_table_widget.setRowCount(len(pending_booking_items))
            for row, booking in enumerate(pending_booking_items):
                self.pending_table_widget.setItem(row, 0, QTableWidgetItem(booking.customer.fullname))
                self.pending_table_widget.setItem(row, 1, QTableWidgetItem(booking.customer.phonenum))
                self.pending_table_widget.setItem(row, 2, QTableWidgetItem(booking.pickup))
                self.pending_table_widget.setItem(row, 3, QTableWidgetItem(booking.dropoff))
                self.pending_table_widget.setItem(row, 4, QTableWidgetItem(booking.formatted_status))

        if assigned_booking_items:
            self.assigned_table_widget.setRowCount(len(assigned_booking_items))
            for row, booking in enumerate(assigned_booking_items):
                self.assigned_table_widget.setItem(row, 0, QTableWidgetItem(booking.customer.fullname))
                self.assigned_table_widget.setItem(row, 1, QTableWidgetItem(booking.customer.phonenum))
                self.assigned_table_widget.setItem(row, 2, QTableWidgetItem(booking.pickup))
                self.assigned_table_widget.setItem(row, 3, QTableWidgetItem(booking.dropoff))
                self.assigned_table_widget.setItem(row, 4, QTableWidgetItem(booking.formatted_status))

        try:
            # Clean up connections/signals if present.
            self.pending_table_widget.itemClicked.disconnect()
            self.assigned_table_widget.itemClicked.disconnect()
        except TypeError:
            pass

        # Show dialog when item is clicked.
        self.assigned_table_widget.itemClicked.connect(
            lambda item: self._show_booking_dialog(assigned_booking_items[item.row()]))
        self.pending_table_widget.itemClicked.connect(
            lambda item: self._show_booking_dialog(pending_booking_items[item.row()]))


    def _show_booking_dialog(self, booking):
        dialog = BookingItem(
            booking=booking,
            viewer="admin",
            parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_scene()

    def switch_to(self, page):
        self.refresh_scene()
        self.admin_stackedWidget.setCurrentWidget(page)

    def refresh_scene(self):
        self.depopulate_data()
        self.populate_data()

    def _log_out(self):
        """Return to launch screen."""
        signals.request_login.emit()
        self.user = None

    def depopulate_data(self):
        self.customer_table_widget.setRowCount(0)
        self.driver_table_widget.setRowCount(0)
        self.assigned_table_widget.setRowCount(0)
        self.pending_table_widget.setRowCount(0)

    def populate_data(self):
        if self.user is None:
            self.info_popup("Could not access your account. Please Try Again or contact Support.")
            signals.request_login.emit()
        self._load_users()
        self._load_bookings()
