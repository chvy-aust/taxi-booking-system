from PyQt6.QtWidgets import QLineEdit, QVBoxLayout, QHBoxLayout

from database.db import DatabaseConnection
from src.app.scenes.base import BaseScene
from src.app.widgets.button import Button
from src.app.widgets.input_edit import InputEdit


class LoginScene(BaseScene):
    def __init__(self, signals):
        super().__init__(scene_name="login", signals=signals)
        self._load_ui()

    def _load_ui(self):
        self.email = InputEdit("Enter email address:")
        self.password = InputEdit("Enter password:")

        # Add buttons to container.
        self.back_btn =  Button("Return to Main Menu", self._return_to_menu)
        self.login_btn = Button("Login", self._start_login)
        btn_continer = QHBoxLayout()
        btn_continer.addWidget(self.back_btn)

        # Set layout to scene.
        container = QVBoxLayout()
        container.addWidget(self.email)
        container.addWidget(self.password)


        container.addLayout(btn_continer)
        self.setLayout(container)

    def _return_to_menu(self):
        self.signals.request_splash.emit()

    def _start_login(self):
        # Get user input from fields.
        user_input = self._get_input()

        # Select user from database using email value.
        try:
            with DatabaseConnection() as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM users WHERE email = ?", (user_input['email'],))

                result = cursor.fetchone()

                if result and result[0] == user_input['password']:
                    print("Login successful")
                else:
                    print("Invalid email or password.")

        except Exception as e:
            print(e)

    def _get_input(self):
        values = {
            self.email: self.email.text().lower(),
            self.password: self.password.text()
        }
        return values