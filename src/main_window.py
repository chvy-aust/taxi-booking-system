import logging

from PyQt6.QtWidgets import QMainWindow, QApplication, QStackedWidget

from src.core.models import User
from src.scenes import (
    RegisterScene, LoginScene,
    CustomerDashboardScene, BaseScene)
from src.signals import signals
from src.utils.constants import STYLE_FILE

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """
    Main window class for the taxi booking class.
    Handles window styling, configuration and scene management.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AC Taxi Services")
        self.setFixedSize(770, 600)
        self.scene_manager = QStackedWidget()

        # Store application scenes.
        self.scenes = {
            "login": LoginScene(),
            "register": RegisterScene(),
            "customer_dash": CustomerDashboardScene(),
        }

        for scene in self.scenes:
            self.scene_manager.addWidget(self.scenes[scene])

        # Listen for signals.
        self._handle_signals()

        # Set scene manager + styling..
        self._center_window()
        self._set_style()
        self.setCentralWidget(self.scene_manager)

    def _handle_signals(self):
        """Respond to signals emitted from scenes."""
        signals.request_register.connect(lambda: self._switch_to('register'))
        signals.request_login.connect(lambda: self._switch_to('login'))

        signals.request_customer_dash.connect(
            lambda user: self._switch_to('customer_dash', user)
        )


    def _switch_to(self, scene_name: str, data: User | None = None):
        """Navigate to requested scene and populate data if provided."""
        # Clean up current scene.
        self.scene_manager.currentWidget().depopulate_data()

        # Switch scene.
        scene = self.scenes[scene_name]
        if data:
            scene.user = data
            scene.populate_data()
        self.scene_manager.setCurrentWidget(scene)
        scene.refresh_scene()

    def _center_window(self):
            """Center main window on screen."""
            # Get primary screen's center (x, y) from application.
            center = QApplication.primaryScreen().availableGeometry().center()
            window = self.frameGeometry()
            # Set window's center to screen's center
            window.moveCenter(center)
            # Move window to center.
            self.move(window.topLeft())

    def _set_style(self):
        """Read style sheet and apply to application."""
        with open(STYLE_FILE, 'r') as file:
            style_sheet = file.read()
        self.setStyleSheet(style_sheet)