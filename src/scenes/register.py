import sqlite3
from typing import override

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

from database.db import DatabaseConnection
from src.scenes import BaseScene
from src.utils.constants import ErrorMessage
from src.widgets import Button
from src.widgets.user_form import UserForm


class RegisterScene(BaseScene):
    """Register scene class for the application."""

    def __init__(self, signals):
        super().__init__(
            scene_name="register",
            signals=signals)
        self.signals = signals
        self._load_ui()

    @override
    def _load_ui(self):
        """Setup UI."""
        # Register scene header label.
        header = QLabel("Create a new Account")
        header.setObjectName("HEADER")
        header.setFixedHeight(80)

        # Custom divider.
        divider = QWidget()
        divider.setObjectName("DIVIDER")
        divider.setFixedHeight(3)

        # Set user form..
        self.form = UserForm(self)
        self.form.setObjectName("register_form")

        # Make buttons.
        back_btn = Button("Return to Main Menu", self._return_to_menu)
        register_btn = Button("Register", self._start_registration)

        # Add buttons to container.
        btns = QHBoxLayout()
        btns.addWidget(back_btn)
        btns.addStretch()
        btns.addWidget(register_btn)

        # Add all elements to scene's layout.
        container = QVBoxLayout()
        container.addWidget(header)
        container.addWidget(divider)
        container.addWidget(self.form)
        container.addLayout(btns)

        # Set layout to scene.
        self.setLayout(container)

    def _return_to_menu(self):
        self.signals.trigger_refresh.emit()
        self.signals.request_splash.emit()

    def _start_registration(self):
        """Start the registration process."""
        # Get credentials from fields.
        values = self.form.get_credentials()
        # If credentials not valid, terminate process.
        if values is None:
            return

        try:
            # Save user to database.
            with DatabaseConnection() as conn:
                conn.create_user(
                    values["firstname"],
                    values["lastname"],
                    # Convert QDate to str.
                    values["dob"].toString("yyyy-MM-dd"),
                    values["phonenum"],
                    values["email"],
                    values["address"],
                    values["create_pass"],)
        except sqlite3.Error:
            self.critical_popup(ErrorMessage.DATABASE_ERROR)
        else:
            self.info_popup("Successfully registered! Redirecting back to landing screen…")
            self._return_to_menu()

    @override
    def refresh_scene(self):
        """Remove error hinting and clear fields."""
        self.form.reset_fields()












