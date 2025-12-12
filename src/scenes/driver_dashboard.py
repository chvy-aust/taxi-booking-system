import sqlite3

from PyQt6.QtWidgets import QTableWidgetItem

from src.core.database import DatabaseConnection
from src.scenes import BaseScene
from src.signals import signals
from src.ui import UiDriverDashboard
from src.widgets import SystemFeedback


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

        #ASSIGNED DRIVES TABLE
        self.assign_table_widget.setColumnCount(5)
        self.assign_table_widget.setHorizontalHeaderLabels(["Name", "Phone", "Pickup", "Destination", "Status"])
        self.assign_table_widget.verticalHeader().hide()

        #COMPLETED DRIVES TABLE
        self.completed_table_widget.setColumnCount(5)
        self.completed_table_widget.setHorizontalHeaderLabels(["Name", "Phone", "Pickup", "Destination", "Status"])
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


        self.assigned_trips_btn.clicked.connect(lambda: self.switch_to(self.view_trip_page))
        self.back_to_home_btn_3.clicked.connect(lambda: self.switch_to(self.driver_home_page))

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
        active_booking, past_bookings = None, []
        try:
            with DatabaseConnection() as conn:
                bookings = conn.fetch_bookings(driver_id=self.user.id)
                for booking in bookings:
                    if booking.status in ("cancelled", "completed"):
                        past_bookings.append([
                            booking.id, booking.customer_id, booking.pickup,
                            booking.dropoff, booking.status, booking.date,
                        ])
                    if booking.status in ("waiting_for_pickup", "in_process"):
                        active_booking = [
                            booking.id, booking.customer_id,
                            booking.pickup, booking.dropoff, booking.status
                        ]
        except sqlite3.Error:
            self.info_popup(SystemFeedback.DATABASE_ERROR)


        # Populate active bookings (Can only have one booking at a time.)
        ACTIVE_BOOKING_HEADERS = ['ID', 'Customer', 'Pickup', 'Dropoff', 'Status']
        self.assign_table_widget.setColumnCount(len(ACTIVE_BOOKING_HEADERS))
        self.assign_table_widget.setHorizontalHeaderLabels(ACTIVE_BOOKING_HEADERS)
        if active_booking:
            self.assign_table_widget.setRowCount(1)
            for column_index, value in enumerate(active_booking):
                self.assign_table_widget.setItem(
                    0, column_index, QTableWidgetItem(str(value)))

        # Populate past bookings
        PAST_BOOKING_HEADERS = ACTIVE_BOOKING_HEADERS + ['Date']
        self.completed_table_widget.setColumnCount(len(PAST_BOOKING_HEADERS))
        self.completed_table_widget.setHorizontalHeaderLabels(PAST_BOOKING_HEADERS)
        if past_bookings:
            self.completed_table_widget.setRowCount(len(past_bookings))
            for row, booking in enumerate(past_bookings):
                for column_index, value in enumerate(booking):
                    self.completed_table_widget.setItem(
                        row, column_index, QTableWidgetItem(str(value)))

    def _log_out(self):
        """Return to launch screen."""
        signals.request_login.emit()
        self.user = None

    def depopulate_data(self):
        pass

    def populate_data(self):
        if self.user is None:
            self.info_popup(
                "Could not access your account. Please Try Again or contact Support.")
            signals.request_login.emit()
        self._load_bookings()