import sqlite3

from PyQt6 import uic
from PyQt6.QtWidgets import QLineEdit

from src.core.database import DatabaseConnection
from src.scenes import BaseScene
from src.signals import signals
from src.widgets import SystemFeedback


class LoginScene(BaseScene):
    def __init__(self):
        super().__init__(scene_name="login")
        uic.loadUi("src/ui/login.ui", self)
        # Hide password characters
        self.password.set_echo_mode(QLineEdit.EchoMode.Password)

        # Setup button events
        self.signup_link.clicked.connect(self._trigger_register)
        self.login_btn.clicked.connect(self._start_login)

    def _trigger_register(self):
        """Navigate to register scene."""
        self._reset_fields()
        signals.request_register.emit()

    def _start_login(self):
        user_input = {
            "email": self.email.text().lower(),
            "password": self.password.text()
        }

        try:
            with DatabaseConnection() as conn:
                user = conn.lookup_user(user_input['email'])
                if user and user.password == user_input['password']:
                    self.info_popup("Login successful")
                    self._switch_to_dashboard(user)
                else:
                    self.info_popup("Invalid email or password.")
        except sqlite3.Error:
            self.info_popup(SystemFeedback.DATABASE_ERROR)


    def _reset_fields(self):
        """Cleanup text left in fields."""
        self.email.reset()
        self.password.reset()

    def _switch_to_dashboard(self, user):
        """Enforce RBA and navigate to required dashboard."""
        self._reset_fields()
        if user.role == "admin":
            signals.request_admin_dash.emit(user)
        elif user.role == "driver":
            signals.request_driver_dash.emit(user)
        elif user.role == "customer":
            signals.request_customer_dash.emit(user)
        else:
            self.info_popup("Could not navigate to dashboard.")
