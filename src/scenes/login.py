import sqlite3

from PyQt6.QtWidgets import QLineEdit

from src.core.database import DatabaseConnection
from src.scenes import BaseScene
from src.signals import signals
from src.ui.ui_login import UiLogin
from src.widgets import SystemFeedback


class LoginScene(BaseScene, UiLogin):
    def __init__(self):
        super().__init__("login")
        self.setupUi(self)
        # Hide password characters
        self.password.set_echo_mode(QLineEdit.EchoMode.Password)
        # Setup button events
        self.login_btn.clicked.connect(self._start_login)
        self.signup_link.clicked.connect(signals.request_register.emit)


    def _start_login(self):
        email = self.email.text().lower()
        password = self.password.text()

        try:
            with DatabaseConnection() as conn:
                user = conn.fetch_users(email=email)[0]
                if user and user.password == password:
                    self.info_popup("Login successful")
                    self._switch_to_dashboard(user)
                else:
                    self.info_popup("Invalid email or password.")
        except sqlite3.Error:
            self.info_popup(SystemFeedback.DATABASE_ERROR)

    def _switch_to_dashboard(self, user):
        """Enforce RBA and navigate to required dashboard."""
        if user.role == "admin":
            signals.request_admin_dash.emit(user)
        elif user.role == "driver":
            signals.request_driver_dash.emit(user)
        elif user.role == "customer":
            signals.request_customer_dash.emit(user)
        else:
            self.info_popup("Could not access user information.")

    def populate_data(self):
        self.email.set_focus()

    def depopulate_data(self):
        """Cleanup text left in fields."""
        self.email.reset()
        self.password.reset()
