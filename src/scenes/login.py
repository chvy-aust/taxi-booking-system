import sqlite3

from PyQt6.QtWidgets import QLineEdit

from ..core import DatabaseConnection
from ..scenes import BaseScene
from ..signals import signals
from ..ui import UiLogin
from ..utils.constants import USER_DB_ERROR, USER_ACCOUNT_DB_ERROR


class LoginScene(BaseScene, UiLogin):
    def __init__(self):
        super().__init__("login")
        self.setupUi(self)
        self._load_ui()

    def _load_ui(self):
        """Hide password characters + setup button events."""
        self.password.set_echo_mode(QLineEdit.EchoMode.Password)
        self.login_btn.clicked.connect(self._start_login)
        self.signup_link.clicked.connect(signals.request_register.emit)

    def _start_login(self):
        """Collect user-input and validate credentials."""
        email = self.email.text().lower()
        password = self.password.text()

        try:
            with DatabaseConnection() as conn:
                results = conn.fetch_users(email=email)
                user = results[0] if results else None
                # Raise verification error if email or password is invalid.
                if not user or user.password != password:
                    self.info_popup("Invalid email or password.")
                    return
                # Otherwise continue login.
                self.info_popup("Login successful")
                self._switch_to_dashboard(user)
        except sqlite3.Error:
            self.info_popup(USER_DB_ERROR)

    def _switch_to_dashboard(self, user):
        """Enforce RBA and navigate to required dashboard."""
        if user.role == "admin":
            signals.request_admin_dash.emit(user)
        elif user.role == "driver":
            signals.request_driver_dash.emit(user)
        elif user.role == "customer":
            signals.request_customer_dash.emit(user)
        else:
            self.info_popup(USER_ACCOUNT_DB_ERROR)

    def populate_data(self):
        self.email.set_focus()

    def depopulate_data(self):
        """Cleanup text left in fields."""
        self.email.reset()
        self.password.reset()
