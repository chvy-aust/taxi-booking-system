import sqlite3

from PyQt6.QtWidgets import QTableWidgetItem, QDialog

from src.core.database import DatabaseConnection
from src.scenes import BaseScene
from src.signals import signals
from src.ui import UiDriverDashboard
from src.widgets import SystemFeedback, BookingItemDialog


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

        #ASSIGNED DRIVES TABLE
        ASSIGN_TABLE_HEADERS = ["Name", "Phone", "Pickup", "Destination", "Status"]
        self.assign_table_widget.setColumnCount(len(ASSIGN_TABLE_HEADERS))
        self.assign_table_widget.setHorizontalHeaderLabels(ASSIGN_TABLE_HEADERS)
        self.assign_table_widget.verticalHeader().hide()

        #COMPLETED DRIVES TABLE
        COMPLETED_TABLE_HEADERS = ASSIGN_TABLE_HEADERS + ['Date']
        self.completed_table_widget.setColumnCount(len(COMPLETED_TABLE_HEADERS))
        self.completed_table_widget.setHorizontalHeaderLabels(COMPLETED_TABLE_HEADERS)
        self.completed_table_widget.verticalHeader().hide()

        self.load_trip_data()

    #--- LOAD DATA FROM DATABASE TO TABLE
    def load_trip_data(self):
        connection = sqlite3.connect("taxibooking.db")
        cur = connection.cursor()

        #COME BACK AND CHECK QUERY
        #sqlquery = "SELECT C.FIRSTNAME, C.PHONENUM, T.PICKUP, T.DROPOFF FROM bookings T JOIN users C ON T.CUSTOMER_ID = C"

        self.assign_table_widget.setRowCount(25)
        self.completed_table_widget.setRowCount(25)

        assigned_table_row = 0
        completed_table_row = 0

        #for row in cur.execute(sqlquery):
            #status = row[4].lower()

            #if status == "pending":
                #table = self.assign_table_widget
                #current_row = assigned_table_row
                #assigned_table_row += 1
            #elif status == "completed":
                #table = self.completed_table_widget
                #current_row = completed_table_row
                #completed_table_row += 1
            #else:
                #continue

            #table.insertRow(current_row)
            #table.setItem(current_row, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            #table.setItem(current_row, 1, QtWidgets.QTableWidgetItem(row[1]))
            #table.setItem(current_row, 2, QtWidgets.QTableWidgetItem(row[3]))
            #table.setItem(current_row, 3, QtWidgets.QTableWidgetItem(row[2]))
            #table.setItem(current_row, 4, QtWidgets.QTableWidgetItem(row[4]))

        #connection.close()

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
        current_booking, assigned_booking_item, past_booking_items = None, [], []
        try:
            with DatabaseConnection() as conn:
                bookings = conn.fetch_bookings(driver_id=self.user.id)
                for booking in bookings:
                    if booking.status in ("cancelled", "completed"):
                        past_booking_items.append([
                            booking.customer.fullname,
                            booking.customer.phonenum,
                            booking.pickup, booking.dropoff,
                            booking.status.replace("_", " ").title(),
                            booking.date
                        ])
                    if booking.status in ("waiting_for_pickup", "in_process"):
                        assigned_booking_item = [
                            booking.customer.fullname,
                            booking.customer.phonenum,
                            booking.pickup, booking.dropoff,
                            booking.status.replace("_", " ").title()
                        ]
                        current_booking = booking
        except sqlite3.Error:
            self.info_popup(SystemFeedback.DATABASE_ERROR)

        # Populate active bookings (Should only have one booking at a time.)
        if assigned_booking_item:
            self.assign_table_widget.setRowCount(1)
            for column_index, value in enumerate(assigned_booking_item):
                self.assign_table_widget.setItem(
                    0, column_index, QTableWidgetItem(str(value)))

            # Clean up connections/signals if present.
            try:
                self.assign_table_widget.cellClicked.disconnect()
            except TypeError:
                pass
            # Show dialog when item is clicked.
            self.assign_table_widget.cellClicked.connect(
                lambda:self._show_booking_dialog(current_booking))

        # Populate past bookings
        if past_booking_items:
            self.completed_table_widget.setRowCount(len(past_booking_items))
            for row, booking in enumerate(past_booking_items):
                for column_index, value in enumerate(booking):
                    self.completed_table_widget.setItem(
                        row, column_index, QTableWidgetItem(str(value)))

    def _show_booking_dialog(self, booking):
        dialog = BookingItemDialog(booking, self)
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