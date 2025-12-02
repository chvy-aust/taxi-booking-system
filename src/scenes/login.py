import sqlite3

from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QWidget

from src.core.database import DatabaseConnection
from src.scenes import BaseScene
from src.widgets import Button, InputEdit
from src.widgets import SystemFeedback
from src.signals import signals


class LoginScene(BaseScene):
    def __init__(self):
        super().__init__(scene_name="login")
        self._load_ui()

    def _load_ui(self):

        header = QLabel("LOG IN")
        header.setObjectName("HEADER")
        header.setFixedHeight(80)

        # Custom divider.
        divider = QWidget()
        divider.setObjectName("DIVIDER")
        divider.setFixedHeight(3)

        self.email = InputEdit("Enter email address:")
        self.password = InputEdit("Enter password:")
        self.password.set_echo_mode(QLineEdit.EchoMode.Password)

        # Add buttons to container.
        self.back_btn =  Button("Sign Up", self._trigger_register)
        self.login_btn = Button("Login", self._start_login)
        btn_continer = QHBoxLayout()
        btn_continer.addWidget(self.back_btn)
        btn_continer.addWidget(self.login_btn)

        # Set layout to scene.
        container = QVBoxLayout()
        container.addWidget(header)
        container.addWidget(divider)
        container.addWidget(self.email)
        container.addWidget(self.password)
        container.addLayout(btn_continer)
        self.setLayout(container)

    def _trigger_register(self):
        self._reset_fields()
        signals.request_register.emit()

    def _start_login(self):
        # Get user input from fields.
        user_input = self._get_input()

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


    def _get_input(self):
        values = {
            "email": self.email.text().lower(),
            "password": self.password.text()
        }
        return values

    def _reset_fields(self):
        self.email.reset()
        self.password.reset()

    def _switch_to_dashboard(self, user):
        self._reset_fields()
        if user.role == "admin":
            signals.request_admin_dash.emit(user)
        elif user.role == "driver":
            signals.request_driver_dash.emit(user)
        elif user.role == "customer":
            signals.request_customer_dash.emit(user)
        else:
            self.info_popup("Could not navigate to dashboard.")
