import sqlite3

from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QWidget

from database.db import DatabaseConnection
from src.scenes import BaseScene
from src.widgets import Button, InputEdit
from src.models import User
from src.dialogs import SystemFeedback


class LoginScene(BaseScene):
    def __init__(self, signals):
        super().__init__(scene_name="login", signals=signals)
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
        self.back_btn =  Button("Return to Main Menu", self._return_to_menu)
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

    def _return_to_menu(self):
        self._reset_fields()
        self.signals.request_splash.emit()

    def _start_login(self):
        # Get user input from fields.
        user_input = self._get_input()

        try:
            with DatabaseConnection() as conn:
                result = conn.lookup_user(user_input['email'])
                if result and result['password'] == user_input['password']:
                    self.info_popup("Login successful")
                    self._switch_to_dashboard(result)
                else:
                    self.info_popup("Invalid email or password.")
        except sqlite3.Error:
            self.critical_popup(SystemFeedback.DATABASE_ERROR)


    def _get_input(self):
        values = {
            "email": self.email.text().lower(),
            "password": self.password.text()
        }
        return values

    def _reset_fields(self):
        self.email.reset()
        self.password.reset()

    def _switch_to_dashboard(self, data):
        self._reset_fields()
        user = User(data)
        if user.role == "admin":
            self.signals.request_admin_dash.emit(user)
        elif user.role == "driver":
            self.signals.request_driver_dash.emit(user)
        elif user.role == "customer":
            self.signals.request_customer_dash.emit(user)
        else:
            self.critical_popup("Could not navigate to dashboard.")
