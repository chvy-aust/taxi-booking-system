import sqlite3

from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QDialog

from src.core.database import DatabaseConnection
from src.scenes import BaseScene
from src.signals import signals
from src.ui import UiDriverDashboard
from src.widgets import SystemFeedback, BookingItem


class DriverDashboardScene(BaseScene, UiDriverDashboard):
    """
    View controller for the Driver Dashboard.
    Inherits from base scene and pyuic6 converted UI file.
    """
    def __init__(self):
        super().__init__("driver-dashboard")
        self.setupUi(self)

        # HOME BTN + LOGOUT BTN  + MENU BTN-----
        # --- button events (switch to panel)
        self.driver_home_bn.clicked.connect(lambda: self.switch_to(self.driver_home_page))
        self.driver_logout_btn.clicked.connect(self._log_out)

        # VIEW ASSIGNED RIDES PAGE -----
        # --- button events (switch to panel)
        self.assigned_trips_btn.clicked.connect(lambda: self.switch_to(self.view_trip_page))
        self.back_to_home_btn_3.clicked.connect( lambda: self.switch_to(self.driver_home_page))

        ASSIGN_TABLE_HEADERS = ["Name", "Phone", "Pickup", "Destination", "Status"]
        self.assign_table_widget.setColumnCount(len(ASSIGN_TABLE_HEADERS))
        self.assign_table_widget.setHorizontalHeaderLabels(ASSIGN_TABLE_HEADERS)
        self.assign_table_widget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.assign_table_widget.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.assign_table_widget.verticalHeader().hide()

        COMPLETED_TABLE_HEADERS = ASSIGN_TABLE_HEADERS
        self.completed_table_widget.setColumnCount(len(COMPLETED_TABLE_HEADERS))
        self.completed_table_widget.setHorizontalHeaderLabels(COMPLETED_TABLE_HEADERS)
        self.completed_table_widget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.completed_table_widget.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.completed_table_widget.verticalHeader().hide()

    def switch_to(self, page):
        self.refresh_scene()
        self.driver_stackedWidget.setCurrentWidget(page)

    def refresh_scene(self):
        self.depopulate_data()
        self.populate_data()

    def _load_bookings(self):
        """
        Fetch and load driver bookings.
        Displays currently assigned booking + past bookings onto TableView.
        """
        current_booking, assigned_booking, past_booking_items = None, [], []
        try:
            with DatabaseConnection() as conn:
                bookings = conn.fetch_bookings(driver_id=self.user.id)
                for booking in bookings:
                    if booking.status in ("cancelled", "completed"):
                        past_booking_items.append(booking)
                    else:
                        assigned_booking = booking
        except sqlite3.Error:
            self.info_popup(SystemFeedback.DATABASE_ERROR)

        # Populate active bookings (Should only have one booking at a time.)
        if assigned_booking:
            self.assign_table_widget.setRowCount(1)
            # Name column
            self.assign_table_widget.setItem(
                0, 0, QTableWidgetItem(assigned_booking.customer.fullname))
            # Phonenum column
            self.assign_table_widget.setItem(
                0, 1, QTableWidgetItem(assigned_booking.customer.phonenum))
            # Pickup location column
            self.assign_table_widget.setItem(
                0, 2, QTableWidgetItem(assigned_booking.pickup))
            # Destination column
            self.assign_table_widget.setItem(
                0, 3, QTableWidgetItem(assigned_booking.dropoff))
            # Booking status column
            self.assign_table_widget.setItem(
                0, 4, QTableWidgetItem(assigned_booking.get_formatted_status))

        if past_booking_items:
            self.completed_table_widget.setRowCount(len(past_booking_items))
            for row, booking in enumerate(past_booking_items):
                # Name column
                self.completed_table_widget.setItem(
                    row, 0, QTableWidgetItem(booking.customer.fullname))
                # Phonenum column
                self.completed_table_widget.setItem(
                    row, 1, QTableWidgetItem(booking.customer.phonenum))
                # Pickup location column
                self.completed_table_widget.setItem(
                    row, 2, QTableWidgetItem(booking.pickup))
                # Destination column
                self.completed_table_widget.setItem(
                    row, 3, QTableWidgetItem(booking.dropoff))
                # Booking status column
                self.completed_table_widget.setItem(
                    row, 4, QTableWidgetItem(booking.get_formatted_status))

        try:
            # Clean up connections/signals if present.
            self.assign_table_widget.itemClicked.disconnect()
            self.completed_table_widget.itemClicked.disconnect()
        except TypeError:
            pass
        # Show dialog when item is clicked.
        self.assign_table_widget.itemClicked.connect(
            lambda: self._show_booking_dialog(assigned_booking))
        self.completed_table_widget.itemClicked.connect(
            lambda item: self._show_booking_dialog(
                past_booking_items[item.row()])
        )

    def _show_booking_dialog(self, booking):
        dialog = BookingItem(
            booking=booking,
            viewer="driver",
            parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_scene()

    def _log_out(self):
        """Return to launch screen."""
        signals.request_login.emit()
        self.user = None

    def depopulate_data(self):
        # Clear bookings populated on tables
        self.assign_table_widget.setRowCount(0)
        self.completed_table_widget.setRowCount(0)

    def populate_data(self):
        if self.user is None:
            self.info_popup(
                "Could not access your account. Please Try Again or contact Support.")
            signals.request_login.emit()
        self._load_bookings()