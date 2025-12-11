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
        self.customer_table_widget.setColumnCount(5)
        self.customer_table_widget.setHorizontalHeaderLabels(["User ID", "Name", "Email", "Phone","Role"])
        self.load_data()

    #--- LOAD DATA FROM DATABASE TO TABLE
    def load_data(self):
        connection = sqlite3.connect("taxibooking.db")
        cur = connection.cursor()
        sqlquery = "SELECT ID,FIRSTNAME, PHONENUM, EMAIL, ROLE FROM user"

        self.customer_table_widget.setRowCount(100)
        self.customer_table_widget.verticalHeader().hide()
        tablerow = 0
        for row in cur.execute(sqlquery):
            self.customer_table_widget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.customer_table_widget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.customer_table_widget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.customer_table_widget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.customer_table_widget.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[4]))
            tablerow += 1
        connection.close()

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
