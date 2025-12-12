from src.signals import signals
from src.scenes import BaseScene
from src.ui import UiAdminDashboard
import sqlite3
from PyQt6 import QtWidgets


class AdminDashboardScene(BaseScene, UiAdminDashboard):
    """
    View controller for the Admin Dashboard.
    Inherits from base scene and pyuic6 converted UI file.
    """
    def __init__(self):
        super().__init__("admin-dashboard")
        self.setupUi(self)

        # HOME BTN + LOGOUT BTN  + MENU BTN-----
        # --- button events (switch to panel)
        self.admin_home_bn.clicked.connect(lambda: self.switch_to(self.admin_home_page))
        self.admin_logout_btn.clicked.connect(self._log_out)

        # ASSIGN DRIVER PAGE -----
        # --- button events (switch to panel)
        self.assign_drivers_btn.clicked.connect(lambda: self.switch_to(self.assign_drivers_page))
        self.cancel_assignment_btn.clicked.connect(lambda: self.switch_to(self.admin_home_page))

        # VIEW USERS PAGE -----
        # --- button events (switch to panel)
        self.view_users_btn.clicked.connect(lambda: self.switch_to(self.view_users_page))
        self.back_to_home_btn.clicked.connect(lambda: self.switch_to(self.admin_home_page))


        # --- VIEW USERS TABLE SETUP

        #VIEW CUSTOMER TABLE
        self.customer_table_widget.setColumnCount(5)
        self.customer_table_widget.setHorizontalHeaderLabels(["User ID", "Name", "Email", "Phone","Role"])
        self.customer_table_widget.verticalHeader().hide()

        #VIWE DRIVERS TABLE
        self.driver_table_widget.setColumnCount(5)
        self.driver_table_widget.setHorizontalHeaderLabels(["User ID", "Name", "Email", "Phone", "Role"])
        self.driver_table_widget.verticalHeader().hide()
        self.load_data()

    #--- LOAD DATA FROM DATABASE TO TABLE
    def load_data(self):
        connection = sqlite3.connect("taxibooking.db")
        cur = connection.cursor()
        sqlquery = "SELECT ID, FIRSTNAME, PHONENUM, EMAIL, ROLE FROM users"

        self.customer_table_widget.setRowCount(25)
        self.driver_table_widget.setRowCount(25)

        customer_table_row = 0
        driver_table_row = 0

        for row in cur.execute(sqlquery):
            user_role = row[4].lower()
            if user_role == "customer":
                table = self.customer_table_widget
                current_row = customer_table_row
                customer_table_row += 1

            elif user_role == "driver":
                table = self.driver_table_widget
                current_row = driver_table_row
                driver_table_row += 1
            else:
                continue  # Skip unknown roles

            table.insertRow(current_row)
            table.setItem(current_row, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            table.setItem(current_row, 1, QtWidgets.QTableWidgetItem(row[1]))
            table.setItem(current_row, 2, QtWidgets.QTableWidgetItem(row[3]))
            table.setItem(current_row, 3, QtWidgets.QTableWidgetItem(row[2]))
            table.setItem(current_row, 4, QtWidgets.QTableWidgetItem(row[4]))
        connection.close()

        # --- ASSIGN DRIVERS SETUP

        #TO BE COMPLETED DRIVES TABLE
        self.pending_table_widget.setColumnCount(5)
        self.pending_table_widget.setHorizontalHeaderLabels(["Name", "Email", "Phone","Pickup","Destination", "Status"])
        self.pending_table_widget.verticalHeader().hide()

        #DRIVER'S COMPLETED DRIVES TABLE
        self.complete_admin_table_widget.setColumnCount(5)
        self.complete_admin_table_widget.setHorizontalHeaderLabels(["Name", "Email", "Phone","Pickup","Destination", "Status"])
        self.complete_admin_table_widget.verticalHeader().hide()
        #self.load_data_assign()

    # --- LOAD DATA FROM DATABASE TO TABLE
    #def load_data_assign(self):
        #connection = sqlite3.connect("taxibooking.db")
        #cur = connection.cursor()
        #sqlquery = "SELECT........FROM ........"

        self.pending_table_widget.setRowCount(20)
        self.complete_admin_table_widget.setRowCount(20)

        #pending_table_row = 0
        #completed_table_row = 0

        #for row in cur.execute(sqlquery):
            #status = row[5].lower()
            #if status == "pending":
                #table = self.pending_table_widget
                #current_row = pending_table_row
                #pending_table_row += 1

            #elif status == "completed":
                #table = self.complete_admin_table_widget
                #current_row = completed_table_row
                #completed_table_row += 1
            #else:
                #continue  # Skip unknown roles

            #table.insertRow(current_row)
            #table.setItem(current_row, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            #table.setItem(current_row, 1, QtWidgets.QTableWidgetItem(row[1]))
            #table.setItem(current_row, 2, QtWidgets.QTableWidgetItem(row[3]))
            #table.setItem(current_row, 3, QtWidgets.QTableWidgetItem(row[2]))
            #table.setItem(current_row, 4, QtWidgets.QTableWidgetItem(row[4]))
        #connection.close()




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
        pass

    def populate_data(self):
        if self.user is None:
            self.info_popup("Could not access your account. Please Try Again or contact Support.")
            signals.request_login.emit()
