import sqlite3
from typing import override

from PyQt6.QtWidgets import QVBoxLayout

from database.db import DatabaseConnection
from src.app.scenes.base import BaseScene
from src.app.widgets import InputEdit, DateEdit, Button
from src.models import User
from src.utils import FieldHints


class CustomerDashboardScene(BaseScene):
    def __init__(self, signal):
        super().__init__("dashboard", signals=signal)
        self._load_ui()

    def _load_ui(self):
        # Buttons
        self.logout_btn = Button("Log out", self._log_out)


    def _log_out(self):
        self.user = None
        self.signals.request_splash.emit()

    def _update_user(self):
        # accept user fields, update here.
        try:
            with DatabaseConnection() as conn:
                # update user in db and return row obj -> conn.update()
                print("something happens here")
                # set updated user on scene -> call self.user.update() <- add method to update user obj
        except sqlite3.Error as e:
            self.critical_popup(
                "Database Error",
                f"A database exception occurred during this process. Data was not updated.")
            return
        else:
            self.info_popup("Successfully updated profile!")
            # re-populate data ->  call self.signals.trigger_refresh.emit()

    @override
    def refresh_scene(self):
        self.populate_data()

    @override
    def populate_data(self):
        if self.user is None:
            self.critical_popup("User data could not be loaded!")
            return

        # Fields to populate here:
